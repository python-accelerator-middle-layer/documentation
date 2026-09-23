# Control Modes

A control mode is one way of accessing the accelerator. pyAML is built so that the core interactions with the machine work in exactly the same way in every control mode. The following requirements guide the design:

- Core interactions work identically in all control modes.
- All configured control modes are available at all times, and can be used at the same time in one script.
- All control modes are defined in the configuration.
- Standard measurements and high-level applications behave in the same way in every control mode.

## Available Control Modes

Two kinds of control modes are implemented today.

**Live** (`ControlSystem`)
: Access to the accelerator through its control system. The values are read from and written to the control system through control-system bindings such as `tango-pyaml` or `pyaml-cs-oa`. The control system can be the real machine or a *virtual accelerator*, a simulation exposed through the same control-system interface as the real machine. By convention this mode is named `live`.

**Design** (`Simulator`)
: Access to a simulation of the accelerator. Values are read from and written to a [pyAT](https://atcollab.github.io/at/p/index.html) lattice. Diagnostics such as BPMs and tune monitors return the values computed by the simulator. No control system is needed. By convention this mode is named `design`.

The modes are declared in the configuration: control systems in `controls` and simulators in `simulators`. Each of them has a `name`, which is also the name of the attribute used to access it:

```yaml
class: pyaml.accelerator.Accelerator
facility: My facility
machine: sr
energy: 1.0e9
simulators:
  - class: pyaml.lattice.simulator.Simulator
    name: design
    lattice: ${path:sr_lattice.json}
controls:
  - class: pyaml_cs_oa.controlsystem.OphydAsyncControlSystem
    name: live
    catalog: catalog.yaml
```

```python
accelerator.design  # the Simulator
accelerator.live    # the ControlSystem
```

Several simulators or control systems can be defined, as long as they have different names. For example a second simulator loaded with a lattice including errors could be named `errors` and reached with `accelerator.errors`.

## Using Control Modes

Because every mode exposes the same elements, arrays and tools, a script can be written once and run in any mode:

```python
def correct_tune(sr):
    sr.tune.set([0.2, 0.3])

correct_tune(accelerator.design)  # try it on the simulator first
correct_tune(accelerator.live)    # then run it on the machine
```

A common pattern is to select the mode once at the top of a script:

```python
SR = accelerator.design   # switch to accelerator.live to act on the machine
```

Different modes can also be used side by side, for example to compare the measured orbit with the simulated one:

```python
delta = (
    accelerator.live.bpms.get("BPM").positions.get()
    - accelerator.design.bpms.get("BPM").positions.get()
)
```

or to copy the corrector settings of the machine into the model:

```python
hcorr = accelerator.live.magnets.get("HCorr").strengths.get()
accelerator.design.magnets.get("HCorr").strengths.set(hcorr)
```

## Planned Control Modes

```{admonition} Planned, not implemented yet
:class: note

The following control modes are described in the pyAML specification. They are part of the long-term plan of the collaboration and are **not available yet**.
```

**Errors / commissioning simulations**
: Simulators with lattices containing errors, and arrays of randomly generated error seeds, used to run simulated commissioning of a machine.

**Shadow (digital shadow)**
: A simulator that follows the real machine: settings read from the control system are applied to the model, which then computes the expected optics and diagnostics. Writing is forbidden in this mode.

**Archive**
: A simulator loaded with the machine settings found in the archiving system at a given time, to reproduce and investigate a past situation.
