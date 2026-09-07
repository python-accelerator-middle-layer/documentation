# Control System Catalogs

As pyAML is control-system agnostic, communication with different control systems is handled through control-system bindings. The bindings handle the details of reading from and writing to each backend.

Since the configuration for the bindings varies between backends and can be verbose, it has been separated into a catalog. The catalog allows simple keys to be used in the accelerator configuration and maps each key to the corresponding backend signal configuration, for example a TANGO attribute or an EPICS PV.

The catalog can be viewed as a simple database of control-system signal configurations. It can contain signals that are not currently used by pyAML, and it can be maintained separately from the pyAML configuration if preferred.

There are two types of catalogs: dynamic and static. These will be explained in detail below.

## The Role of the Catalog

The definition of which catalog to use is done at the control system level.

For example:

```
controls:
- class: tango.pyaml.controlsystem.TangoControlSystem
  name: live
  catalog: fodo_1gev_6d_pyaml_catalogs.yaml
```

It is possible to refer to the same catalog for several control systems.

An entry in the catalog can for example look like:

```
class: tango.pyaml.static_catalog.StaticCatalog
entries:
- class: tango.pyaml.static_catalog_entry.StaticCatalogEntry
  key: AN01-AR/EM-QP/QF.01/magnetic_strength
  device:
    class: tango.pyaml.attribute.Attribute
    attribute: AN01-AR/EM-QP/QF.01/magnetic_strength
    unit: 1/m
```

Devices in the accelerator configuration can then refer to the entry by using the key `AN01-AR/EM-QP/QF.01/magnetic_strength`.

When the information is needed, the control system backend will ask the catalog to resolve the key, get the configuration information and use it to create the desired backend signal.

## Dynamic Catalog

The dynamic catalog allows to read configuration information directly from an external control system. This requires access to the control system of the machine but is convenient if you already have configuration information stored in your control system and want to avoid having to maintain a separate catalog for pyAML. For example, it is possible to read configuration information directly from the TANGO database.

## Static Catalog

A static catalog does not require access to a control system. In this version, all the configuration information is defined directly in the catalog.