# Create and Load Configuration

The principles and syntax of the configuration are explained in more detail in [Principles and Syntax of the Configuration](../../explanation/configuration). This guide focuses on the different ways to create it.

There are several ways to create a configuration. It is recommended to test the different options and see which one you prefer:

- [Use ConfigurationSchema](./use-configuration-schema.ipynb) objects and export as a dictionary or text file

- Use a JSON Schema in the [MetaConfigurator](./use-meta-configurator.md)

- Use a [JSON Schema in VS Code](./use-vscode-json-schema.md)

## Load the Configuration

The configuration can be loaded into the `Accelerator` in several ways:

| Type| Command | Description |
| --- | --- | --- |
| File | `Accelerator.load()` | A text file in JSON on YAML format.
| Dictionary | `Accelerator.from_dict()` | A nested dictionary.

## Validation

The configuration is validated when loading it into the `Accelerator` but it can also be validated without having to load it. This is useful if you want to be able to maintain it separately from pyAML. See [Validate Configuration](./validate-configuration) for details.