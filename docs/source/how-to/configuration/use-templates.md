# Use Configuration Templates

Use a template when several devices share the same configuration and only names or catalog keys differ. Define the common fields once, then supply the differences as arguments.

## Define and Use a Template

Save this complete example as `accelerator.yaml`:

```yaml
class: pyaml.accelerator.Accelerator
facility: my_facility
machine: storage_ring
energy: 1.0e9
controls:
 - class: tango.pyaml.controlsystem.TangoControlSystem
   tango_host: my_host
   name: live
   catalog:
     class: tango.pyaml.tango_catalog.TangoCatalog
     disconnected: True
templates:
  - name: quadrupole
    parameters: 
      - name
      - catalog_key
    config:
      class: pyaml.magnet.quadrupole.Quadrupole
      name: "{name}"
      model:
        class: pyaml.magnet.identity_model.IdentityMagnetModel
        unit: 1/m
        physics: "domain/family/{catalog_key}/strength"
devices:
  - ${template:quadrupole,QF_001,QF.01}
  - ${template:quadrupole,QD_001,QD.01}
```

Each template has a unique `name`, an ordered list of `parameters`, and a `config` body. 

```{warning}
Unquoted braces can be interpreted as YAML syntax. For example, `name: {name}` creates a mapping with the key `name` and a null value, rather than the string placeholder intended for substitution. You can write `name: "{name}"` instead. Always quote strings containing substitution placeholders to avoid mistakes.
```

Each `${template:NAME,args}` call inserts a copy of the body with its placeholders replaced. Here, the first argument sets the device name and the second supplies the non-repeatable part of the catalog key prefix. The result is two quadrupoles, `QF_001` and `QD_001`, with their own model configurations.

## Example to run:

Run the example in Python with the following snippet (requires `tango-pyaml`):

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from pyaml.accelerator import Accelerator

configuration = """
class: pyaml.accelerator.Accelerator
facility: my_facility
machine: storage_ring
energy: 1.0e9
controls:
 - class: tango.pyaml.controlsystem.TangoControlSystem
   tango_host: my_host
   name: live
   catalog:
     class: tango.pyaml.tango_catalog.TangoCatalog
     disconnected: True
templates:
  - name: quadrupole
    parameters: 
      - name
      - catalog_key
    config:
      class: pyaml.magnet.quadrupole.Quadrupole
      name: "{name}"
      model:
        class: pyaml.magnet.identity_model.IdentityMagnetModel
        unit: 1/m
        physics: "domain/family/{catalog_key}/strength"
devices:
  - ${template:quadrupole,QF_001,QF.01}
  - ${template:quadrupole,QD_001,QD.01}
"""

with TemporaryDirectory() as directory:
    path = Path(directory) / "accelerator.yaml"
    path.write_text(configuration, encoding="utf-8")

    accelerator = Accelerator.load(str(path))
    print(accelerator.live["QF_001"])
    print(accelerator.live["QD_001"])
```

For a lower-level loading behavior and explanation, see [Configuration Templates](../../explanation/configuration.md#configuration-templates).
