# Write Documentation

The documentation for pyAML has been separated into parts to make it more modular and easier to maintain. The documentation consists of:

- **Ecosystem documentation**: contains documentation for the whole ecosystem. This includes tutorials, how-to guides and explanation.

    This documentation is hosted in its own repository and published to GitHub pages. Information about how to contribute and build it is available in the repository README.

    Repository: <https://github.com/python-accelerator-middle-layer/documentation>  
    GitHub page: <https://python-accelerator-middle-layer.github.io/documentation/>. 

- **Package documentation**: each package also its own documentation. This is primarily meant for API documentation but can also include other parts if needed for that specific package.  

  This documentation is hosted inside the package repository. It is built and published by [readthedocs](https://about.readthedocs.com/) to allow to publish several versions. For it to automatically build, the repository needs to be linked to a project on readthedocs.
  
  On readthedocs it is possible to configure to build on pull requests. If this has been activated a link appears in the GitHub pull request where you can view the built documentation as part of the review.

  A template for the package documentation is included in the [pyaml-repository-template](https://github.com/python-accelerator-middle-layer/pyaml-repository-template) which can be used to add documentation for a new package.
  
## Docstring Format

PyAML uses NumPy style docstrings. An example of the format is available at [Example NumPy Style Python Docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html).

For pyAML the following has been decided:

- Classes should have a class level docstring. This should include description of the class, list of constructor parameters and an example configuration if the class can be included in the configuration. If using the documentation template, docstrings in the `__init__` will be ignored.

- Attributes, properties and methods should have their own docstrings.

If you follow these guidelines the documentation will look nice both when building the readthedocs and when the users use `help` in the Python environment.