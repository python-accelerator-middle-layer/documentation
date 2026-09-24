# Create and Load Configuration

This guide shows how to write a pyAML configuration as a text file and load it into an `Accelerator`.

```{tip}
Read [Configuration Structure and Syntax](../../explanation/configuration) which explains the concepts and ideas behind the configuration before you start.
```

## The Rule to Remember

```{important}
Each item of the configuration names a Python class in its `class` field. **Every other field is an argument of the constructor of that class**, with the same name. When an argument is an object, its value is a nested item with its own `class` field.
```

Writing a configuration is therefore the same as writing the Python code that creates the objects, in YAML (or JSON) instead of Python.

## Find the Fields of a Class

Before writing an item, look up the constructor arguments of its class. Any of these works:

- `help()` in Python, which shows the constructor signature and describes each argument:

  ```python
  from pyaml.bpm.bpm import BPM

  help(BPM)
  # class BPM(...)
  #  |  BPM(name: str, lattice_names: str | None = None, description: str | None = None,
  #  |      x_pos: str | None = None, y_pos: str | None = None, ...)
  #  |
  #  |  Parameters
  #  |  ----------
  #  |  name : str
  #  |      Name of the BPM.
  #  |  x_pos : str | None, optional
  #  |      Device catalog key for the horizontal beam position.
  #  |  ...
  ```

- the [API documentation](https://pyaml.readthedocs.io/en/stable/) of the class,
- the `describe()` method of the schema in the [schema registry](./use-schema-registry.ipynb).

Arguments without a default value (here `name`) are required fields; the others can be left out.

## Write the Configuration File

Create a file, for example `accelerator.yaml`, with any text editor. The steps below build a small but complete configuration, using the names of the [test lattice](../../tutorials/functionality/01_create_accelerator).

### 1. The Accelerator

The root item is the `Accelerator`. Its required arguments are `facility`, `machine` and `energy`:

```yaml
class: pyaml.accelerator.Accelerator
facility: My facility
machine: sr
energy: 1.0e9
```

### 2. The Control Modes

Add the control modes as lists in `simulators` and `controls`. Their `name` is also the name used to access them (`accelerator.design`, `accelerator.live`).

A simulator needs the path to a lattice file. Use `${path:...}` so that the path is resolved relative to the [configuration root](../../explanation/configuration.md#configuration-root) and the lattice is not loaded as a configuration file:

```yaml
simulators:
  - class: pyaml.lattice.simulator.Simulator
    name: design
    lattice: ${path:lattice.json}
```

A control system is given by the class of the bindings you use. Its arguments depend on the bindings, for example for `pyaml-cs-oa`:

```yaml
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    backend: tango
    catalog: catalog.yaml
```

The catalog describes how the keys used by the devices map to control-system signals. It follows exactly the same rule. A static catalog for `pyaml-cs-oa` looks like this (one entry per key):

```yaml
class: pyaml_cs_oa.static_catalog.StaticCatalog
entries:
  - class: pyaml_cs_oa.static_catalog_entry.StaticCatalogEntry
    key: AN01-AR/EM-QP/QF.01/magnetic_strength
    device:
      class: pyaml_cs_oa.tangoAtt.TangoAtt
      attribute: AN01-AR/EM-QP/QF.01/magnetic_strength
      unit: 1/m
  # ... one entry for each key used in the configuration
```

See [Control System Catalogs](../../explanation/catalog.md) for the different types of catalogs. If you only want to use the simulator, you can leave out `controls` entirely.

### 3. The Devices

Add the elements of the machine in `devices`. For a magnet, the `model` argument is an object (the magnet model, which also handles the unit conversion), so it is written as a nested item:

```yaml
devices:
  - class: pyaml.magnet.quadrupole.Quadrupole
    name: QF_001
    model:
      class: pyaml.magnet.identity_model.IdentityMagnetModel
      unit: 1/m
      physics: AN01-AR/EM-QP/QF.01/magnetic_strength
  - class: pyaml.magnet.quadrupole.Quadrupole
    name: QD_001
    model:
      class: pyaml.magnet.identity_model.IdentityMagnetModel
      unit: 1/m
      physics: AN01-AR/EM-QP/QD.01/magnetic_strength
  - class: pyaml.bpm.bpm.BPM
    name: BPM_001
    x_pos: AN01-AR/DG-EPOS/BPM.01/x
    y_pos: AN01-AR/DG-EPOS/BPM.01/y
```

By default, the `name` of an element is also the name of the element in the lattice of the simulator. Use `lattice_names` if they differ. The strings given to `physics`, `x_pos` and `y_pos` are keys looked up in the catalog of the control system.

### 4. The Arrays

Group elements in named arrays in `arrays`. Element names can contain wildcards:

```yaml
arrays:
  - class: pyaml.arrays.magnet.Magnet
    name: Quadrupoles
    elements:
      - QF_001
      - QD_001
  - class: pyaml.arrays.bpm.BPM
    name: BPMs
    elements:
      - BPM_*
```

### Complete File

Putting it all together:

```yaml
class: pyaml.accelerator.Accelerator
facility: My facility
machine: sr
energy: 1.0e9
simulators:
  - class: pyaml.lattice.simulator.Simulator
    name: design
    lattice: ${path:lattice.json}
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    backend: tango
    catalog: catalog.yaml
devices:
  - class: pyaml.magnet.quadrupole.Quadrupole
    name: QF_001
    model:
      class: pyaml.magnet.identity_model.IdentityMagnetModel
      unit: 1/m
      physics: AN01-AR/EM-QP/QF.01/magnetic_strength
  - class: pyaml.magnet.quadrupole.Quadrupole
    name: QD_001
    model:
      class: pyaml.magnet.identity_model.IdentityMagnetModel
      unit: 1/m
      physics: AN01-AR/EM-QP/QD.01/magnetic_strength
  - class: pyaml.bpm.bpm.BPM
    name: BPM_001
    x_pos: AN01-AR/DG-EPOS/BPM.01/x
    y_pos: AN01-AR/DG-EPOS/BPM.01/y
arrays:
  - class: pyaml.arrays.magnet.Magnet
    name: Quadrupoles
    elements:
      - QF_001
      - QD_001
  - class: pyaml.arrays.bpm.BPM
    name: BPMs
    elements:
      - BPM_*
```

## Split the Configuration into Several Files

For a real machine the configuration becomes long. When the configuration is loaded from a file, any string value ending with `.yaml`, `.yml` or `.json` is replaced by the content of that file (this is how `catalog: catalog.yaml` above is loaded). Inside a list, if the file contains a list, its items are added to the parent list. For example, move the quadrupoles to `devices/quadrupoles.yaml`:

```yaml
# devices/quadrupoles.yaml
- class: pyaml.magnet.quadrupole.Quadrupole
  name: QF_001
  model:
    class: pyaml.magnet.identity_model.IdentityMagnetModel
    unit: 1/m
    physics: AN01-AR/EM-QP/QF.01/magnetic_strength
- class: pyaml.magnet.quadrupole.Quadrupole
  name: QD_001
  # ...
```

and refer to it from the main file:

```yaml
devices:
  - devices/quadrupoles.yaml
  - class: pyaml.bpm.bpm.BPM
    name: BPM_001
    x_pos: AN01-AR/DG-EPOS/BPM.01/x
    y_pos: AN01-AR/DG-EPOS/BPM.01/y
```

Values can also come from environment variables with `${env:NAME}`. See [Resolvers](../../explanation/configuration.md#resolvers) for all options.

## Use Your Own Classes

The rule is not limited to pyAML classes. Any class that can be imported can be used in the configuration, for example a magnet model specific to your facility:

```python
# my_facility/models.py
from pyaml.magnet.model import MagnetModel

class MyMagnetModel(MagnetModel):
    def __init__(self, power_supply: str, calibration: float):
        ...
```

```yaml
model:
  class: my_facility.models.MyMagnetModel
  power_supply: PS/QF/01
  calibration: 1.02
```

## Load the Configuration

Set the configuration root, which is the directory used to resolve relative paths, then load the file with `Accelerator.load()`:

```python
from pyaml.configuration import ROOT
from pyaml.accelerator import Accelerator

ROOT.set("/path/to/configuration")
accelerator = Accelerator.load("accelerator.yaml")

accelerator.design.magnets.get("Quadrupoles").strengths.get()
```

If the control-system bindings are not installed or you only want to use the simulator, add `ignore_external=True`. The `controls` section is then skipped.

The configuration can also be given as a nested dictionary with `Accelerator.from_dict()`, following the same rule:

```python
import yaml

with open("accelerator.yaml") as file:
    config = yaml.safe_load(file)

accelerator = Accelerator.from_dict(config)
```

See the API documentation for the [Accelerator](https://pyaml.readthedocs.io/en/stable/api/pyaml.accelerator.html#module-pyaml.accelerator) for all options.

## Validate the Configuration

Each item is checked when it is created: a missing required field or an unknown field raises a `PyAMLConfigException` naming the class and the field. The whole configuration can also be validated before anything is created, which gives all errors at once:

```python
from pyaml.validation import SchemaRegistry

SchemaRegistry().discover()
accelerator = Accelerator.load("accelerator.yaml", validate=True)
```

The configuration can also be validated without loading it, which is useful if you maintain it separately from pyAML. See [Validate Configuration](./validate-configuration).

## Tools That Help Writing the Configuration

Writing the file by hand is often the simplest way to start, but tools based on a [JSON Schema](../../explanation/schema_and_validation.md) can suggest the available fields and check their types while you write:

- [Use a JSON Schema in VS Code](./use-vscode-json-schema.md)
- [Use the MetaConfigurator](./use-meta-configurator.md), a form-based editor in the browser
- [Use ConfigurationSchema](./use-configuration-schema.ipynb) objects to create the configuration in Python and export it as a dictionary or text file

AI coding assistants can also help: supply for example a lattice file, a description of the naming conventions of your control system, and the JSON Schema of the pyAML configuration.

For information about JSON Schemas and how to generate them, see [Configuration Schemas and Validation](../../explanation/schema_and_validation.md) and [Generate JSON Schemas](./generate-json-schema.ipynb).
