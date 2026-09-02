# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: pyaml-documentation
#     language: python
#     name: python3
# ---

# %%
"""
Creating an Accelerator
==========================================================

This tutorial shows the different ways to create a pyAML accelerator.
The example only uses the simulator mode. The other modes are explored in other tutorials.

The first approach constructs the objects interactively whereas the second one creates them
by loading a configuration file. Both produce the same final interface, but each is suited
to different use cases which will be explained in the tutorial.
"""

# %%
# Prerequisites
# -------------
#
# This tutorial requires a lattice file in a format supported by
# `pyAT <https://atcollab.github.io/at/p/index.html>`_.
#
# The example uses the lattice provided by the ``pyaml-test-lattice`` package.

# Get the path to the lattice file
from pyaml_test_lattice import lattice_file
lattice_filepath = lattice_file

# %%
# Approach 1: Interactive Creation
# ------------------------------------
#
# In the first approach the different parts of the accelerator is created interactively.
# In this example we will only create a single quadrupole magnet to use with the simulator mode.

# %%
# Create a Quadrupole Magnet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

from pyaml.magnet.identity_model import IdentityMagnetModel
from pyaml.magnet.quadrupole import Quadrupole
from pyaml.lattice.simulator import Simulator

# Create a model for the magnet
model = IdentityMagnetModel(physics='')

# Create the quadrupole
quad = Quadrupole(name="QF_001", model=model)

# Create the simulator
simulator = Simulator(name="design", lattice=str(lattice_filepath))

# Attach the quadrupole to the simulator
simulator.fill_device([quad])
quad = simulator.magnet.get("QF_001")

# %%
# Read and Set the Quadrupole Strength
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print(f"Initial strength: {quad.strength.get()}")

quad.strength.set(0.504)

print(f"Updated strength: {quad.strength.get()}")

# %%
# Create an Accelerator
# ~~~~~~~~~~~~~~~~~~~~~
# You can also create an accelerator.
#
# This is not strictly necessary for this simple example with only a single device.
# However, it provides an interface for adding metadata,
# supporting multiple control modes, and grouping devices.
#
# The features of the accelerator is explored in other tutorials.

from pyaml.accelerator import Accelerator

simulator._MAGNETS.pop("QF_001", None)
simulator._ALL.pop("QF_001", None)

accelerator = Accelerator(
    facility="pyAML_test_facility",
    machine="pyaml_test_machine",
    energy=1e9,
    simulators=[simulator],
    devices=[quad]
)

# Get the quadrupole
quad = accelerator.design.magnet.get("QF_001")

# Read the strength in the same way as before 
quad.strength.get()


# %%
# Approach 2: Load a Configuration
# -------------------------------------
# Devices can also be created by loading a configuration file.
#
# Configuration files are loaded through the interface of the accelerator and 
# are intended to be used for use cases with many devices, several control modes etc.
#
# Configuration files can be written in YAML or JSON. This example shows a YAML file.


# %%
# Create a YAML file
# ~~~~~~~~~~~~~~~~~~
# The YAML file can be created using different tools. More details can be found in the the how-to guides.
# In this example we create it directly here.

import yaml

data = {
    "type": "pyaml.accelerator",
    "facility": "pyAML test facility",
    "machine": "pyaml test machine",
    "data_folder": None,
    "energy": None,
    "simulators": [
        {
            "type": "pyaml.lattice.simulator",
            "lattice": "${env:PYAML_TEST_LATTICE}",
            "name": "design",
        }
    ],
    "devices": [
        {
            "type": "pyaml.magnet.quadrupole",
            "name": "QF_001",
            "model": {
                "type": "pyaml.magnet.identity_model",
                "physics": "",
            },
        }
    ],
}

with open("config.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(data, file, sort_keys=False)

# %%
# Specify the Path to the Configuration File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The path to the configuration file can be specified as absolute or relative to a root directory.

# Set the root directory
from pathlib import Path
from pyaml.configuration import ROOT

current_dir = Path.cwd()
ROOT.set(current_dir)

# Display the loaded content
config_path = Path('config.yaml')
print(config_path.read_text())


# %%
# Specify the Path to the Lattice File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The path to the lattice file can be specified in the configuration file
# as absolute or relative to the root directory.
#
# It is also possible to specify it using an environment variable.
# The syntax for that is shown in this example.

import os
os.environ["PYAML_TEST_LATTICE"] = str(lattice_file)

# %%
# Create an Accelerator
# ~~~~~~~~~~~~~~~~~~~~~
from pyaml.accelerator import Accelerator

accelerator = Accelerator.load('config.yaml')

# Get the quadrupole
quad = accelerator.design.magnet.get('QF_001')

# Use the quadrupole in the same way as before
quad.strength.get()

# %%
