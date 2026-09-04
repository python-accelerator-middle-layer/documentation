# Create Configuration

By creating a configuration it is possible to have pyAML create devices and applications automatically for several control modes.

There are different ways to create a configuration and different formats are supported.
These are explained in this guide.

## Principle

The configuration is done on the level of an `Accelerator`. This allows not only to create devices and applications for different control modes but also to define parameters and metadata which are common for the accelerator.

The syntax supports configuration of both pyAML classes and third party classes to allow the use of pyAML implementations as well as facility specific implementation in the same accelerator. This is done by for each item in the configuration define the field `class` or `class_path` to say which class to build an object of.

## Format Options

A configuration can be created and loaded using different formats:

1. File

    The configuration can be written as a text file and loaded using `Accelerator.load()`. Both `YAML` and `JSON` are supported but `YAML` is considered the default option.

2. Dictionary

    The configuration can be written as a nested dictionary and loaded using `Accelerator.from_dict()`.


To be continued with details about the different tools to help write it...
