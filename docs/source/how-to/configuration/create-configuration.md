# Create and Load Configuration

This guide shows how to write a pyAML configuration and load it into an `Accelerator`. It gives recommendations for how to write it and list tools that are available to help.

```{tip}
Read [Configuration Structure and Syntax](../../explanation/configuration) which explains the concepts and ideas behind the configuration before you start.
```
The configuration can be written as a text file in YAML or JSON or as a dictionary.

## The Rule to Remember

The configuration consists of a set of items which tells pyAML which objects to build when loading the configuration.

```{important}
Each item of the configuration names a Python class in its `class` field. **Every other field is an argument of the constructor of that class** with the same name as the field and the value to pass to the constructor. When a constructor argument is an object, its value in the configuration is a nested item with its own `class` field.
```

Writing and loading the configuration is the equivalent of writing the Python code that creates the objects yourself. The configuration just allows pyAML to create the objects for you.

## Finding the Accepted Fields

Before writing an item, look up the constructor parameters of the class you want pyAML to build an object of. This can be done in several ways:

- Read the [API documentation](./../reference/index.md) of the class
- Use `help()` in Python since this shows the signature of the constructor and description of each parameter

For example:

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

- Use the schema registry. The `describe()` method lists the fields of a registered class with their types. See [Use the Schema Registry](../how-to/configuration/use-schema-registry.ipynb).
- Use a JSON Schema in an external tool. See [JSON Schema Tools](../how-to/configuration/create-configuration.md#tools-that-help-writing-the-configuration).

Parameters with a default value is optional and can be left out of the configuration if you wish.

## Write Configuration as a Text File

Here an example is shown for how to create the configuration in a YAML file. The steps are similar if using JSON. The steps below build a small but complete configuration, using the names of the [test lattice](../../tutorials/functionality/01_create_accelerator).

Create a file, for example `accelerator.yaml`, with any text editor. If you want the editor to suggest the fields, you can use VS Code together with a JSON Schema. See [Use JSON Schema in VS Code](../configuration/use-vscode-json-schema.md) for instructions.

### 1. The Accelerator

The root item is the `Accelerator`. Its required arguments are `facility`, `machine` and `energy`:

```yaml
class: pyaml.accelerator.Accelerator
facility: my_facility
machine: storage_ring
energy: 1.0e9
```

### 2. The Control Modes

Add the control modes as lists in `simulators` and `controls`. Their `name` is also the name used to access them, for example `accelerator.design`, `accelerator.live` etc.

A simulator needs the path to a lattice file. All [formats that can be loaded by pyAT](https://atcollab.github.io/at/p/api/at.load.html#module-at.load) works. If you use the JSON format, you need to use the `${path:...}` [resolver](../../explanation/configuration.md#resolvers) to avoid the lattice being loaded as if it was a configuration file.

```yaml
simulators:
  - class: pyaml.lattice.simulator.Simulator
    name: design
    lattice: ${path:lattice.json}
```

A control system is given by the class of the bindings you use. The arguments depend on the bindings and catalog type you decide to use. The catalog describes how the keys used by the devices map to control-system signals. See [Control System Catalogs](../../explanation/catalog.md) for the different types of catalogs.

For example for `pyaml-cs-oa` using a dynamic catalog for TANGO:

```yaml
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    backend: tango
```

If you only want to use the simulator, you can leave out `controls` entirely.

### 3. The Devices

Add the elements of the machine in `devices`. For a magnet, the `model` argument is an object (the magnet model, which also handles the unit conversion), so it is written as a nested item.

The strings given to `physics`, `x_pos` and `y_pos` are keys looked up in the catalog of the control system.

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

By default, the `name` of an element is also the name of the element in the lattice of the simulator. If you want to use a different name in pyAML, use `lattice_names` to map between pyAML and the lattice.

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
facility: my_facility
machine: storage_ring
energy: 1.0e9
simulators:
  - class: pyaml.lattice.simulator.Simulator
    name: design
    lattice: ${path:lattice.json}
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    backend: tango
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

For a real machine the configuration becomes long. When the configuration is loaded from a file, any string value ending with `.yaml`, `.yml` or `.json` is replaced by the content of that file. Inside a list, if the file contains a list, its items are added to the parent list. For example, move the quadrupoles to `devices/quadrupoles.yaml`:

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
