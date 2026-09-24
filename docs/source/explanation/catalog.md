# Control System Catalogs

As pyAML is control-system agnostic, communication with different control systems is handled through control-system bindings. The bindings handle the details of reading from and writing to each control system and is implemented in separate packages from the `pyaml` package.

Since the configuration for the bindings varies between backends and can be verbose, it has been separated out from the rest of the pyAML configuration and is handled by the catalog. A catalog is backend specific.

There are two types of catalogs, dynamic and static. They work differently and are intended for different use cases as will be explained below.

The definition of which catalog to use is done at the control system level. It is possible to use to the same catalog for several control systems if you want.

## The Role of the Catalog

Communication with a control system is done using `DeviceAccess` objects. They can represent an EPICS PV, TANGO attribute or other backend-specific signal.

The catalog makes it possible to use simple keys in the pyAML configuration and it will retrieve the information needed to build the `DeviceAccess` object, and in some implementations also directly create it. The exact implementation is up to the backend as long as `ControlSystem.get_device_access` returns the `DeviceAccess` object for a specific key.

## Dynamic Catalog

```{tip}
The dynamic catalog does not require a configuration file and it is therefore the recommended option for most use cases.
```

In this version, the configuration is extracted from a dynamic source. This can be directly from the control system or some other source, for example a database, depending on the chosen backend and its catalog implementation.

This requires access to the source, for example by being on the same network, but no configuration file for the control system configuration has to be loaded by pyAML.

Example of configuration for dynamic catalog:

```yaml
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    catalog:
      class: pyaml_cs_oa.dynamic_catalog.DynamicCatalog
      backend: tango
```

With `pyaml-cs-oa`, a dynamic catalog is also used when no catalog is given, based on the `backend` field of the control system:

```yaml
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    backend: tango
```

Dynamic catalogs are currently provided by `pyaml-cs-oa`. Check the documentation of your control-system bindings for the catalogs they support.

## Static Catalog

The static catalog is mainly intended for testing purposes. It consists of a file of entries where each entry corresponds to the configuration for a specific key. It can be seen as a simple, static database of control system signal configurations.

The static catalog can contain entries that are not currently used and be maintained separately from the rest of the pyAML configuration if preferred, but it is loaded as part of loading the pyAML configuration.

Example of configuration for static catalog:

```yaml
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    catalog: fodo_1gev_6d_pyaml_catalogs-oa.yaml
```

Example of a static catalog file for `pyaml-cs-oa`, with one entry:

```yaml
class: pyaml_cs_oa.static_catalog.StaticCatalog
entries:
  - class: pyaml_cs_oa.static_catalog_entry.StaticCatalogEntry
    key: AN01-AR/EM-QP/QF.01/magnetic_strength
    device:
      class: pyaml_cs_oa.tangoAtt.TangoAtt
      attribute: AN01-AR/EM-QP/QF.01/magnetic_strength
      unit: 1/m
```

The same catalog for `tango-pyaml` uses the classes of that package (`tango.pyaml.static_catalog.StaticCatalog`, `tango.pyaml.static_catalog_entry.StaticCatalogEntry` and `tango.pyaml.attribute.Attribute`).

This format follows the same syntax as for the rest of the pyAML configuration since during the loading process the file is read and the content added to the rest of the pyAML configuration.