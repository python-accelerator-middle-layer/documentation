# Tools That Help Writing the Configuration

There are tools available to help to write and modify the configuration. They can suggest the fields and check their types while you write. The tools are under development and testing so new or other tools might be available in the future based on user feedback.

Some of the tools are based on a [JSON Schema](https://json-schema.org). For information about JSON Schemas and how to generate them, see [Configuration Schemas and Validation](../../../explanation/schema_and_validation.md) and [Generate JSON Schemas](../generate-json-schema.ipynb).

Currently these tools are available:

- [Use ConfigurationSchema](./use-configuration-schema.ipynb) objects to create the configuration in Python and export it as a dictionary or text file. This allows to program the configuration.

- [Use a JSON Schema in VS Code](./use-vscode-json-schema.md)

- [Use the MetaConfigurator](./use-meta-configurator.md), a form-based editor in the browser

```{tip}
AI coding assistants can also help: supply for example a lattice file, a description of the naming conventions of your control system, and the JSON Schema of the pyAML configuration and ask it to write the configuration for you.
```

```{toctree}
:maxdepth: 1
:hidden:

use-configuration-schema
use-vscode-json-schema
use-meta-configurator
```
