---
html_theme.sidebar_secondary.remove: true
---

# Python Accelerator Middle Layer

Python Accelerator Middle Layer (pyAML) is a joint technology platform for design, commissioning, and operation of particle accelerators.

It is developed by a collaboration of accelerator facilities to give physicists a common, physics-oriented way to access their machines, whether real or simulated, and to share measurement and correction tools between laboratories.

The features include, among others:

- A control system-agnostic interface to interact with the accelerator.
- A common interface to different backends, including a live accelerator, virtual accelerator, and simulator.
- Machine independence, allowing configuration of different types of accelerators using facility-specific naming conventions.
- Unit conversions.
- Automatic generation of metadata and a standardized format for measurement data.
- A set of standard applications and a framework for developing new applications.

```{tip}
Read [What is pyAML?](explanation/about.md) to learn more about the motivation and goals of the project.
```

```{toctree}
:hidden:
:maxdepth: 1

Tutorials <tutorials/index>
how-to/index
explanation/index
reference/index
```

<div style="margin-top: 3rem;"></div>

````{grid} 2
:gutter: 3

```{grid-item-card} New to pyAML?
:link: tutorials/index
:link-type: doc

Learn the fundamentals through a series of step-by-step tutorials.
```

```{grid-item-card} I want to accomplish a task
:link: how-to/index
:link-type: doc

Find practical guides for installation, configuration, and common workflows.
```

```{grid-item-card} I want to understand how it works
:link: explanation/index
:link-type: doc

Read about the design principles, architecture, and concepts behind pyAML.
```

```{grid-item-card} I need package documentation
:link: reference/index
:link-type: doc

Browse the documentation and related packages in the pyAML ecosystem.
```
````