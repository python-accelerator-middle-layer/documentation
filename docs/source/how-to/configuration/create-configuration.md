# Create and Load Configuration

The structure and syntax of the configuration are explained in detail in [Configuration Structure and Syntax](../../explanation/configuration). This guide focuses on the different ways to create it.

There are many ways to create a configuration. It is recommended to test the different
options and see which one you prefer:

- Use a [JSON Schema in VS Code](./use-vscode-json-schema.md)

- Use a JSON Schema in the [MetaConfigurator](./use-meta-configurator.md)

- [Use ConfigurationSchema](./use-configuration-schema.ipynb) objects and export as a dictionary or text file

Another option is to use AI coding assistance tools. You can then for example supply a lattice file, information describing the naming conventions for your control system and a JSON Schema for the pyAML configuration and get help to write it.

For information about what a JSON Schema is and how to generate it, see [Configuration Schemas and Validation](../../explanation/schema_and_validation.md) and [Generate JSON Schemas](./generate-json-schema.ipynb).

## Load the Configuration

The configuration can be loaded into the `Accelerator` in two ways:

| Type| Command | Description |
| --- | --- | --- |
| File | `Accelerator.load()` | A text file in JSON or YAML format.
| Dictionary | `Accelerator.from_dict()` | A nested dictionary.

See the API documentation for the [Accelerator](https://pyaml.readthedocs.io/en/stable/api/pyaml.accelerator.html#module-pyaml.accelerator) for more details.

## Validation

The configuration is validated when loading it into the `Accelerator` but it can also be validated without having to load it. This is useful if you want to be able to maintain it separately from pyAML. See [Validate Configuration](./validate-configuration) for details.