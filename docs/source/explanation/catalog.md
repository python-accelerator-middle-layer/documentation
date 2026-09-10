# Control System Catalogs

As pyAML is control-system agnostic, communication with different control systems is handled through control-system bindings. The bindings handle the details of reading from and writing to each control system and is implemented in separate packages from the `pyaml` package.

Since the configuration for the bindings varies between backends and can be verbose, it has been separated out from the rest of the pyAML configuration and is handled by the catalog. A catalog is backend specific.

There are two types of catalogs, dynamic and static. They work differently and are intended for different use cases as will be explained below.

The definition of which catalog to use is done at the control system level. It is possible to use to the same catalog for several control systems if you want.

## The Role of the Catalog

Communication with a control system is done using `DeviceAccess` objects. They can represent an EPICS PV, TANGO attribute or other backend-specific signal.

The catalog makes it possible to use simple keys in the pyAML configuration and it will retrieve the information needed to build the `DeviceAccess` object, and in some implementations also directly create it. The exact implementation is up to the backend as long as `ControlSystem.get_device_access` returns the `DeviceAccess` object for a specific key.

## Dynamic Catalog

The dynamic catalog does not require a configuration file and it is therefore the recommended option for most use cases.

In this version, the configuration is extracted from a dynamic source. This can be directly from the control system or some other source, for example a database, depending on the chosen backend and its catalog implementation.

This requires access to the source, for example by being on the same network, but no configuration file for the control system configuration has to be loaded by pyAML.

Example of configuration for dynamic catalog:

```yaml
controls:
  - type: pyaml_cs_oa.controlsystem
    name: live
    catalog: 
      - type: pyaml_cs_oa.dynamic_catalog
        backend: tango
```

## Static Catalog

The static catalog is mainly intended for testing purposes. It consists of a file of entries where each entry corresponds to the configuration for a specific key. It can be seen as a simple, static database of control system signal configurations.

The static catalog can contain entries that are not currently used and be maintained separately from the rest of the pyAML configuration if preferred, but it is loaded as part of loading the pyAML configuration.

Example of configuration for static catalog:

```yaml
controls:
- type: pyaml_cs_oa.controlsystem
  name: live
  catalog: fodo_1gev_6d_pyaml_catalogs-oa.yaml
``` 

Example of an entry in the static catalog:

```yaml
class: tango.pyaml.static_catalog.StaticCatalog
entries:
- class: tango.pyaml.static_catalog_entry.StaticCatalogEntry
  key: AN01-AR/EM-QP/QF.01/magnetic_strength
  device:
    class: tango.pyaml.attribute.Attribute
    attribute: AN01-AR/EM-QP/QF.01/magnetic_strength
    unit: 1/m
```

This format follows the same syntax as for the rest of the pyAML configuration since during the loading process the file is read and the content added to the rest of the pyAML configuration.