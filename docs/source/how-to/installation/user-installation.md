# User Installation

The latest release can be installed from PyPI. If you want to communicate with a control system you also need to install the bindings you want by specifing extras.

You need at least Python 3.11.

```{note}
Remember to always install in a virtual environment to avoid breaking your Python environment.
```

## Installing without Control System Bindings

This if for example if you just want to use the simulator.

```
pip install accelerator-middle-layer
```


## Installing with Control System Bindings

Available options for installing with control system bindings are:

- `tango-pyaml` for the tango-pyaml bindings.
-  `cs-oa-epics` for `ophyd-async` bindings with both EPICS channel and PV access.
-  `cs-oa-tango` for `ophyd-async` bindings for TANGO.

Example usage:

```
pip install accelerator-middle-layer[cs-oa-epics]
```


