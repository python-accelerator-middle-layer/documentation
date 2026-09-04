# Configuration Schemas and Validation

In pyAML, schemas are used to describe and validate the data for the configuration. The concept and ideas behind this are explained here. The architecture for the validation contains three components with distinct responsibilities:

- `SchemaRegistry`: discover and store schemas
- `SchemaValidator`: validate configuration data
- `SchemaGenerator`: generate [JSON Schemas](https://json-schema.org/)

## What Is a Schema and Why Use It?

A schema describes the structure of data. This includes permitted fields, values and types. In pyAML, schemas are [Pydantic](https://docs.pydantic.dev/latest/) models which define which fields a configuration object may contain, the type of each field, and validation rules.

This is implemented as a base class `ConfigurationSchema` which defines the minimum required fields for any item in the pyAML configuration. Other schema classes can inherit from this and extend with additional fields.

Every configuration schema has a field `class_path` (with accepted alias `class`) containing the fully qualified class path of the object to construct, for example `mypackage.module.Class`. The configuration can in this way identify both the class and the data needed to create an object.

In addition to this, the configuration schemas can be used to generate [JSON Schemas](https://json-schema.org/). JSON Schema is a common standard used by many tools, and this allows pyAML users to use already existing external tools for writing and validating the pyAML configuration.

## Schema Registration

The `SchemaRegistry` links Python classes to the schema that defines their valid configuration. It maps a fully qualified class path, such as `mypackage.module.Class`, to a `ConfigurationSchema` subclass describing the configuration schema of that class. 

For example:

```text
my_package.devices.Magnet → MagnetConfigurationSchema
```

The registry is an in-memory catalog implemented as a singleton, meaning that creating a schema registry in different parts of pyAML returns the same registry.

Every registered schema must inherit from `ConfigurationSchema` to ensure that the minimum required fields are defined for each item in the registry.

Schemas can be registered manually or be automatically registered during import by using the `register_schema` decorator. It can generate a schema from the class or associate the class with
an explicitly defined schema.

## Schema Validation

The `SchemaValidator` uses the schema registry to find the schema for a specific class. It then validates the data using `Pydantic` and recursively processes nested configuration objects.

## JSON Schema Generation

JSON schemas can be generated using the `SchemaGenerator`. It uses the schema registry to generate JSON schema for the classes registered in the registry. The result can be used by tools such as editors, web interfaces, documentation tools etc which understand JSON schema.

When a schema for a base class has registered schemas for subclasses, the generated schema includes those alternatives as a union.