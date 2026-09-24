# Configuration Structure and Syntax

By creating a configuration it is possible to have pyAML build devices and applications automatically for several control modes.

The configuration is normally written and loaded on the level of an `Accelerator`. This allows to define parameters and metadata which are common for all objects in the accelerator in addition to control modes, arrays and devices. For example:

```yaml
class: pyaml.accelerator.Accelerator
facility: pyAML_facility
machine: storage_ring
data_folder: ''
energy: 1e9
controls:
simulators:
arrays:
devices:
```

The configuration is organised as a description of a nested Python object tree. It contains the information needed to construct the objects.

The syntax has been chosen to allow configuration and construction of objects for both pyAML classes and third party classes. This is to allow integration of facility specific implementation in pyAML, but also to simplify future development where it might be desirable to replace old classes with newer versions without breaking compatibility.

## One Field = One Constructor Argument

The whole configuration follows a single rule:

```{important}
Each configuration item names a Python class in its `class` field. **Every other field of the item is an argument to that class's constructor**, with the same name as the field and the value to be passed to the constructor.
```

The `class` should be written as a fully qualified Python class path, consisting of the module and class name in the format `package.module.Class`.

```{note}
Since `class` is a reserved name in Python, the attribute is called `class_path` in the source code. That is also an accepted alias to use in the configuration.
```

When pyAML reads an item, it imports the class given by `class` and calls it with the remaining fields as keyword arguments. The YAML configuration and Python code below build equivalent objects:

**Configuration**

```yaml
class: pyaml.magnet.quadrupole.Quadrupole
name: QF_001
model:
  class: pyaml.magnet.identity_model.IdentityMagnetModel
  unit: 1/m
  physics: AN01-AR/EM-QP/QF.01/magnetic_strength
```

**Python**

```python
from pyaml.magnet.quadrupole import Quadrupole
from pyaml.magnet.identity_model import IdentityMagnetModel

Quadrupole(
    name="QF_001",
    model=IdentityMagnetModel(
        unit="1/m",
        physics="AN01-AR/EM-QP/QF.01/magnetic_strength",
    ),
)
```

Consequences of this rule:

- **Nested objects are nested items.** If an argument expects an object (here `model` expects a magnet model), the field contains another item with its own `class` field. Lists of objects (such as `devices` or `simulators` of the `Accelerator`) are lists of items.
- **Optional arguments are optional fields.** Arguments with a default value can be left out.
- **Any class can be used.** Nothing is specific to pyAML classes: a facility-specific class from your own package can be used in the same way, as long as it can be imported.

## Separation between Configuration and Source Code

The configuration describes what should be constructed; it does not contain executable Python code. This keeps configuration readable, reviewable, and usable by tools such as JSON Schema editors.

The configuration is possible to maintain separately from pyAML, for example in a separate Git repository or in a database.

## Supported Formats

The configuration can be written and loaded in different formats:

**File**: It can be written as a text file and loaded using `Accelerator.load()`. Both YAML and JSON are supported.

**Dictionary**: It can also be written as a nested dictionary and loaded using `Accelerator.from_dict()`.

## Configuration Root

The configuration root is the directory used to resolve relative configuration paths. It applies to the file passed to `Accelerator.load()` and paths used by [resolvers](#resolvers). Relative paths are resolved against this directory.

By default, the root is the current working directory when pyAML is imported. It can be changed before loading a configuration with `ROOT.set()`:

```python
from pyaml.configuration import ROOT

ROOT.set("/path/to/configuration")
```

After setting the root, a file written as `devices/quadrupole.yaml` in the configuration file will refer to `/path/to/configuration/devices/quadrupole.yaml`.

Setting the root makes it possible to keep a configuration and its included files in a portable directory tree while selecting that tree at runtime.

Absolute paths are normalized and used directly.

## Resolvers

Resolvers can be used in the configuration to let a value refer to information which is supplied when the configuration is loaded, for example an environment variable or another configuration file. A resolver expression has the following form:

```yaml
${resolver:payload}
```

The part before the first colon selects the resolver whereas the part after is passed to that resolver. Expressions are expanded recursively in mappings and lists.

The following built-in resolvers are available:

| Resolver | Type | Description |
| --- | --- | --- |
| `env` | Environment variable | The value of the named environment variable. An error is raised if it is not set. |
| `path` | A file or directory path | The absolute, normalized path, resolved relative to pyAML's configuration root. The target is not loaded as part of loading the configuration. |
| `file` | A YAML, YML, or JSON file path | The path to a file which should be loaded and expanded into the configuration as part of loading it. Relative paths use the configuration root. |

Configuration files can also be included without an explicit `file` expression. A string ending in `.yaml`, `.yml`, or `.json` is loaded automatically for convenience. This makes it easy to split the configuration into several files if one wishes.

```{warning}
If you include a `.yaml`, `.yml`, or `.json` in the configuration file which you do not want to be loaded and expanded into the configuration (for example a lattice in JSON format), remember to put `${path:filename}` or you will get an error when loading the configuration.
```
