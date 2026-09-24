# Glossary

Terms used throughout the pyAML documentation.

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
