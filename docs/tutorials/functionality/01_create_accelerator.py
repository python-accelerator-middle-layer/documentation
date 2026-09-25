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
Create an Accelerator
==========================================================

This tutorial shows the different ways to create a pyAML accelerator.

The example only uses the ``design`` control mode, which is a simulator of the machine based
on pyAT. See :doc:`Introduction to pyAML <00_introduction>` for an
overview of the control modes and the other concepts used here.

The first approach constructs the objects interactively whereas the second one creates them
by loading a configuration file. Both produce the same final interface, but each is suited
to different use cases which will be explained in the tutorial. You will also see that the
two approaches are closely related: **each field of the configuration file is an argument of
the constructor of a Python class**.
"""

# %%
# Prerequisites
# -------------
#
# This tutorial requires a lattice file in a format supported by
# `pyAT <https://atcollab.github.io/at/p/index.html>`_.
#
# The example uses the lattice provided by the ``pyaml-test-lattice`` package.
#
# The Test Lattice
# ~~~~~~~~~~~~~~~~
#
# The test lattice, ``fodo_1gev_6d``, is a small 1 GeV electron storage ring made of
# **16 identical FODO cells** of 4.8 m, for a circumference of 76.8 m. Each cell contains a
# focusing quadrupole ``QF`` and sextupole ``SF``, a beam position monitor ``BPM``, a corrector
# ``COR`` acting in both planes, a dipole ``B``, a defocusing quadrupole ``QD`` and sextupole
# ``SD``, and a second dipole ``B``:
#
# .. figure:: /_static/fodo-cell.svg
#    :alt: Layout of one FODO cell of the test lattice
#    :width: 100%
#
#    One cell of the test lattice with the control-system name of each element
#    (``cc`` is the cell number, from 01 to 16).
#
# Each element is named after its family and a three-digit index equal to the cell number:
# ``QF_001`` is the focusing quadrupole of the first cell. This is the magnet used in
# this tutorial.

# Get the path to the lattice file
# sphinx_gallery_thumbnail_path = '_static/create_accelerator.png'
from pyaml_test_lattice import lattices

# List available files and their descriptions
print(lattices)

lattice_file = lattices['fodo_1gev_6d.json']

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
simulator = Simulator(name="design", lattice=lattice_file)

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

# Recreate the simulator since the accelerator will handle the attachment
simulator = Simulator(name="design", lattice=lattice_file)

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
# The Configuration Rule
# ~~~~~~~~~~~~~~~~~~~~~~
# A configuration file describes the same objects as the ones created in approach 1,
# following one simple rule:
#
# - the ``class`` field gives the full path of the Python class to create,
# - **every other field is an argument of the constructor of that class**, with the same name,
# - when an argument is itself an object, its value is a nested item with its own ``class``.
#
# For example, in approach 1 the quadrupole was created with:
#
# .. code-block:: python
#
#    Quadrupole(name="QF_001", model=IdentityMagnetModel(physics=""))
#
# which becomes in the configuration file:
#
# .. code-block:: yaml
#
#    class: pyaml.magnet.quadrupole.Quadrupole
#    name: QF_001
#    model:
#      class: pyaml.magnet.identity_model.IdentityMagnetModel
#      physics: ''
#
# The accepted fields of any class are therefore given by the arguments of its constructor,
# which you can see with ``help()``. The first lines show the constructor signature, and the
# ``Parameters`` section describes each argument:

help(Quadrupole)

# %%
# Write the Configuration File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# A configuration file is a plain text file. You can write it with any text editor. Other
# tools which can help you are described in the how-to guide
# :doc:`Create and Load Configuration <../../how-to/configuration/create-configuration>`.
#
# The file below describes the same accelerator as in approach 1. Compare each item with
# the Python code above: ``Accelerator(facility=..., machine=..., energy=..., simulators=[...],
# devices=[...])``, ``Simulator(name=..., lattice=...)`` and ``Quadrupole(name=..., model=...)``.
#
# The lattice path is given by an environment variable, using the ``${env:NAME}`` syntax.
# It could also be written directly as an absolute path, or relative to a root directory.

configuration = """\
class: pyaml.accelerator.Accelerator
facility: pyAML test facility
machine: pyaml test machine
energy: 1.0e9
simulators:
  - class: pyaml.lattice.simulator.Simulator
    name: design
    lattice: ${env:PYAML_TEST_LATTICE}
devices:
  - class: pyaml.magnet.quadrupole.Quadrupole
    name: QF_001
    model:
      class: pyaml.magnet.identity_model.IdentityMagnetModel
      physics: ''
"""

with open("config.yaml", "w", encoding="utf-8") as file:
    file.write(configuration)

# %%
# Specify the Paths
# ~~~~~~~~~~~~~~~~~
# The path to the configuration file can be specified as absolute or relative to a root directory.

# Set the root directory
from pathlib import Path
from pyaml.configuration import ROOT

current_dir = Path.cwd()
ROOT.set(current_dir)

# Display the content of the file
config_path = Path('config.yaml')
print(config_path.read_text())

# %%
# Set the environment variable used in the configuration file for the lattice path.

import os
os.environ["PYAML_TEST_LATTICE"] = lattice_file

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
# Mistakes Are Detected
# ~~~~~~~~~~~~~~~~~~~~~
# Since each field must be a constructor argument, a misspelled or unknown field is
# rejected when the configuration is loaded. Here ``phyiscs`` is written instead of ``physics``:

wrong_configuration = configuration.replace("physics:", "phyiscs:")

with open("config.yaml", "w", encoding="utf-8") as file:
    file.write(wrong_configuration)

try:
    Accelerator.load("config.yaml")
except Exception as error:
    print(type(error).__name__)
    print(error)

# Restore the correct configuration file
with open("config.yaml", "w", encoding="utf-8") as file:
    file.write(configuration)
