# What is pyAML?

The Python Accelerator Middle Layer (pyAML) is a Python library that sits between the people who operate or study a particle accelerator and the many systems that make up that accelerator: control systems, simulation codes, archivers, databases, and so on. It is developed by a collaboration of accelerator facilities as a common platform for the design, commissioning, and operation of particle accelerators.

## Why a Middle Layer?

Many accelerator facilities have for years relied on a *Middle Layer*, the MATLAB Middle Layer (MML) being the best-known example. A middle layer gives physicists a uniform, physics-oriented way to access a machine: they read "the orbit at all BPMs" or set "the strength of quadrupole QF1" without having to know which control system variable holds that value, which units it is in, or how a current is converted into a magnetic strength.

pyAML carries that idea forward with a few important changes:

- **Python instead of MATLAB.** Python is open, free and widely used in the scientific community, and it gives access to a large ecosystem of scientific and machine-learning tools.
- **Shared between facilities.** Measurement and correction tools written for pyAML (orbit correction, tune correction, response matrices, etc.) should run at any facility that has configured pyAML, instead of being rewritten at each laboratory.
- **Simulation as a first-class citizen.** The same script can act on the real machine or on a simulated one. Tools can then be developed and tested without using expensive and limited beam time.

## Goals

The collaboration has identified the following key features for pyAML:

- An agnostic interface between an accelerator control system (TANGO, EPICS, ...), a virtual accelerator and a digital model.
- A base for developing and sharing beam measurement tools, such as orbit, trajectory, linear and non-linear optics corrections.
- A virtual accelerator / digital twin which allows testing tuning tools in real-life conditions without the need for beam time.
- Handling of both physics and hardware units, with a flexible unit-conversion interface.
- The possibility to configure different types of accelerators: transfer lines, linear and circular accelerators, and ramped accelerators.
- Configuration and measurement data managed in a standardized manner.
- A set of standard measurement tools in a modular structure.
- Long-term maintainability, by following modern software practices.
- Easy integration of facility-specific functionality as separate packages.

## Layers of the Project

The software is organized in layers:

**Core**
: The features needed to configure a machine and communicate with the different backends: abstraction of devices (magnets, BPMs, tune monitors, ...), grouping of devices in arrays, abstraction of the control system, connection to simulators, and conversion between hardware and physics units. This is the `pyaml` package.

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

## Glossary

Accelerator
: The top-level pyAML object describing one machine (a storage ring, a booster, a transfer line, ...). It holds all the control modes, arrays and devices.

Control mode
: One way of accessing the accelerator, for example `live` (the real machine) or `design` (a simulation). All control modes offer the same interface. See [Control Modes](control-modes.md).

Element
: A single object of the accelerator that can be read or set: a magnet, a BPM, an RF plant, a tune monitor, ...

Array
: A named group of elements, for example all BPMs or all the quadrupoles used for tune correction, that can be read or set in one call.

Tuning tool
: A high-level measurement or correction tool (tune correction, orbit correction, response matrix measurement, ...) configured like any other device.

Backend
: The system that a control mode talks to: a control system (through control-system bindings such as `tango-pyaml` or `pyaml-cs-oa`) or a simulation code (pyAT).

Catalog
: The backend-specific description of how a key used in the configuration maps to a signal of the control system. See [Control System Catalogs](catalog.md).

Virtual accelerator
: A simulated machine exposed through a real control system (for example TANGO devices backed by a simulation), so that it can be used exactly like the real machine.

Digital shadow / digital twin
: A simulation that follows the real machine. In a shadow, changes on the real machine are reflected in the simulation, but not the other way around. In a twin, changes are reflected both ways.
