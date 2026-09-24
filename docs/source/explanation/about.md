# What is pyAML?

The Python Accelerator Middle Layer (pyAML) is an ecosystem of Python packages that provides a common layer between people who operate or study particle accelerators and the different tools they need to work with, such as control systems and simulation codes. It is developed by a collaboration of accelerator facilities as a common framework for the design, commissioning, and operation of particle accelerators.

## Why a Middle Layer?

Many accelerator facilities rely on a *Middle Layer*, with the [MATLAB Middle Layer (MML)](https://github.com/atcollab/MML) being a well-known example at synchrotron light sources.

A middle layer provides a physics-oriented interface to a particle accelerator. It represents the machine in terms of familiar accelerator concepts, such as magnets, BPMs, and RF cavities, while hiding details such as control-system variables, hardware interfaces, units, and conversions from users.

The same interface can be used to interact with either the real accelerator, where values are read from and written to the control system, or a simulated accelerator, where they are obtained from and passed to a simulation code.

PyAML builds on this idea, but is implemented as a modern, Python-based, and extensible framework. Its key characteristics are:

 - **Python-native**: pyAML integrates naturally with the Python scientific ecosystem and the growing number of accelerator-physics tools available in Python.

- **Modular and extensible**: Control systems, simulation codes, and physics applications are connected through well-defined interfaces, allowing new implementations to be added without changing the applications that use them.

- **Configuration-driven**: Accelerator-specific information is kept separate from application code, allowing the same software to be configured for different machines and facilities.

- **Real and virtual machines**: The same interface can be used with the real accelerator, an external digital twin, or an internal simulator, allowing physics applications to work independently of how the accelerator is represented.


## Goals

The collaboration has identified the following key features for pyAML. They are the goals of the project: some of them are already available, others are still being developed.

- An agnostic interface between an accelerator control system (TANGO, EPICS, ...), a virtual accelerator and a digital model.
- A base for developing and sharing beam measurement tools, such as orbit, trajectory, linear and non-linear optics corrections.
- The possibility to use a virtual accelerator or a digital twin, to test tuning tools in real-life conditions without the need for beam time.
- Handling of both physics and hardware units, with a flexible unit-conversion interface.
- The possibility to configure different types of accelerators: transfer lines, linear and circular accelerators, and ramped accelerators.
- Configuration and measurement data managed in a standardized manner.
- A set of standard measurement tools in a modular structure.
- Long-term maintainability, by following modern software practices.
- Easy integration of facility-specific functionality as separate packages.

## Layers of the Project

The software is organized in layers:

**Core**
: The features needed to configure a machine and communicate with the different backends: abstraction of devices (magnets, BPMs, tune monitors, ...), grouping of devices in arrays, the simulator backend based on pyAT, conversion between hardware and physics units, and the *abstract interface* to control systems. This is the `pyaml` package. The actual communication with a given control system is implemented in separate packages, the control-system bindings (`tango-pyaml`, `pyaml-cs-oa`), so that a facility only installs the ones it needs.

**Common high-level applications**
: Tools shared between facilities, built on top of the core: tune and chromaticity correction, response-matrix measurements, orbit correction, dispersion measurement, beam-based alignment, LOCO, etc.

**Facility-specific applications**
: Code developed by a single facility. If it follows the same standards as the rest of pyAML, it can be used together with the core, shared with other facilities, or later moved into the common applications.

See [pyAML Structure](architecture.md) for how these layers map to Python packages and objects.

## Guiding Principles for the Configuration

A facility adopts pyAML by writing a *configuration* describing its machine. The configuration follows these principles:

- It is **completely separated from the source code**. It describes what should be built, it does not contain code.
- It is **easy to extend**. Facility-specific devices can be added without modifying pyAML.
- It is possible to use **only a subset** of it, for example to use a single tool without configuring the whole machine.
- A facility only has to **install the packages it needs**, for example an EPICS facility does not need to install TANGO.

There is one simple rule behind the configuration: each item names a Python class, and each of its other fields is an argument of that class's constructor. See [Configuration Structure and Syntax](configuration.md).

The terms used throughout the documentation are defined in the [Glossary](glossary.md).
