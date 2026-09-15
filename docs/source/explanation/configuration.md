# Configuration Structure and Syntax

By creating a configuration it is possible to have pyAML build devices and applications automatically for several control modes.

The configuration is normally written and loaded on the level of an `Accelerator`. This allows to define parameters and metadata which are common for all objects in the accelerator in addition to control modes, arrays and devices. For example:

```yaml
class: pyaml.accelerator.Accelerator
facility: pyAML_facility
machine: storage_ring
data_folder: ''
energy: 1e6
controls:
simulators:
arrays:
devices:
```

The configuration is organised as a description of a nested Python object tree. It contains the information needed to construct the objects.

The syntax has been chosen to allow configuration and construction of objects for both pyAML classes and third party classes. This is to allow integration of facility specific implementation in pyAML, but also to simplify future development where it might be desirable to replace old classes with newer versions without breaking compatibility.

## Configuration Items

Each configurable item is represented by a mapping which describes the attributes and values needed to construct one Python object. The field `class` or `class_path` identifies the type to construct. It should be written as a fully qualified Python class path, consisting of the module and class name. For example:

```yaml
class: pyaml.magnet.quadrupole.Quadrupole
```

When pyAML reads the configuration, it uses this path to select the class and passes the remaining configuration fields to the constructor of the class.

An object can contain other configurable objects. The nested objects follow the same principle: each has its own `class` field and the values needed to construct it. For example:

```yaml
class: pyaml.magnet.quadrupole.Quadrupole
name: QF_001
model:
  class: pyaml.magnet.identity_model.IdentityMagnetModel
  unit: 1/m
  physics: AN01-AR/EM-QP/QF.01/magnetic_strength
```

## Separation between Configuration and Source Code

The configuration describes what should be constructed; it does not contain executable Python code. This keeps configuration readable, reviewable, and usable by tools such as JSON Schema editors.

The configuration is possible to maintain separately to pyAML, for example in a separate Git repository or in a database.

## Supported Formats

The configuration can be written and loaded in different formats:

**File**: It can be written as a text file and loaded using `Accelerator.load()`. Both `YAML` and `JSON` are supported but `YAML` is considered the default option.

**Dictionary**: It can also be written as a nested dictionary and loaded using `Accelerator.from_dict()`.

## Configuration Root

The configuration root is the directory used to resolve relative configuration paths. It applies to the file passed to `Accelerator.load()`, paths used by resolvers, and automatic file includes. Relative paths are resolved against this directory.

By default, the root is the current working directory when pyAML is imported. It can be changed before loading a configuration with `ROOT.set()`:

```python
from pyaml.configuration import ROOT

ROOT.set("/path/to/configuration")
```

After setting the root, `devices/quadrupole.yaml` refers to `/path/to/configuration/devices/quadrupole.yaml`. Absolute paths are normalized and used directly. Setting the root makes it possible to keep a configuration and its included files in a portable directory tree while selecting that tree at runtime.

## Resolvers

Resolvers let a configuration value refer to information that is supplied when the configuration is loaded, such as an environment variable or another configuration file. A resolver expression has the following form:

```yaml
${resolver:payload}
```

The part before the first colon selects the resolver whereas the part after is passed to that resolver. Expressions are expanded recursively in mappings and lists.

The following built-in resolvers are available:

| Resolver | Type | Description |
| --- | --- | --- |
| `env` | Environment variable | The value of the named environment variable. An error is raised if it is not set. |
| `path` | A file or directory path | The absolute, normalized path, resolved relative to pyAML's configuration root. The target is not loaded as part of loading the configuration. |
| `file` | A YAML, YML, or JSON file path | The path to a file which should be loaded and expanded into the configuration as part of loading the configuration. Relative paths use the configuration root. 

Configuration files can also be included without an explicit `file` expression. A string ending in `.yaml`, `.yml`, or `.json` is loaded automatically for convenience if one wishes to split the configuration into several files.
