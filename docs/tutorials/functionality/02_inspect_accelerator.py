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
Inspect an Accelerator
==========================================================

This tutorial shows how to inspect and access the content of the accelerator.

As a reminder, an accelerator contains one or several control modes (for example ``live``
and ``design``). Each control mode contains the same elements (magnets, BPMs, ...), arrays
(named groups of elements) and tuning tools. See
:doc:`Introduction to pyAML <00_introduction>` for an overview.
"""

# %%
# Prerequisites
# -------------
#
# This tutorial requires an existing pyAML configuration file.
#
# The example uses the configuration provided by the ``pyaml-test-lattice`` package.

# Get the path to the configuration file
# sphinx_gallery_thumbnail_path = '_static/inspect_accelerator.png'
from pyaml_test_lattice import configurations

# List available files and their descriptions
configurations

# %%
# Load the Accelerator
# --------------------

from pyaml.accelerator import Accelerator
accelerator = Accelerator.load(configurations["pyaml/tango/pyaml-cs-oa/fodo_1gev_6d_pyaml-oa.yaml"])

# %%
# About This Configuration
# ------------------------
#
# The configuration describes the test lattice introduced in
# :doc:`Create an Accelerator <01_create_accelerator>`: 16 FODO cells, each containing the
# magnets ``QF``, ``SF``, ``COR``, ``QD``, ``SD`` and a ``BPM``. Elements are named after their
# family and cell number, for example ``QF_001``.
#
# The configuration links each element to its name in the control system, which follows a
# TANGO naming convention of the form ``ANcc-AR/<subsystem>/<family>.01/<attribute>``,
# where ``cc`` is the cell number:
#
# ============  ====================================================
# Element name  Control-system name
# ============  ====================================================
# ``QF_001``    ``AN01-AR/EM-QP/QF.01/magnetic_strength``
# ``QD_001``    ``AN01-AR/EM-QP/QD.01/magnetic_strength``
# ``SF_001``    ``AN01-AR/EM-SX/SF.01/magnetic_strength``
# ``SD_001``    ``AN01-AR/EM-SX/SD.01/magnetic_strength``
# ``COR_001``   ``AN01-AR/EM-COR/CH.01/magnetic_strength`` (horizontal)
#               ``AN01-AR/EM-COR/CV.01/magnetic_strength`` (vertical)
# ``BPM_001``   ``AN01-AR/DG-EPOS/BPM.01/x`` and ``.../BPM.01/y``
# ============  ====================================================
#
# It also defines the following arrays and tuning tools, used in the use-case tutorials:
#
# ========================  ==========================================================
# Name                      Content
# ========================  ==========================================================
# ``Cell1`` ... ``Cell16``  All the elements of one cell
# ``BPM``                   The 16 BPMs
# ``HCorr``, ``VCorr``      The horizontal and vertical correctors
# ``QForTune``              The 32 quadrupoles used for tune correction
# ``BETATRON_TUNE``         The betatron tune monitor
# ``DEFAULT_TUNE_...``      Tune correction and tune response matrix
# ``DEFAULT_ORBIT_...``     Orbit correction and orbit response matrix
# ========================  ==========================================================

# %%
# Inspect the Accelerator Contents
# ------------------------------------
#
# The yellow pages provide an overview of the accelerator.
# This shows what is configured and available for use.

accelerator.yellow_pages

# %%
# Access the Control Modes
# ------------------------
#
# Each control mode is an attribute of the accelerator, named after the mode in the
# configuration. ``modes()`` lists them all.

for name, mode in accelerator.modes().items():
    print(f"accelerator.{name}: {type(mode).__name__}")

# %%
# Show the Configuration of an Array
# ------------------------------------

quads = accelerator.design.magnets.get("QForTune")
print(quads)

# %%
# Show the Configuration of a Magnet in an Array
# -----------------------------------------------

print(quads[0])

# %%
# Find the Accepted Configuration Fields
# --------------------------------------
#
# The configuration fields of the magnet, such as ``name`` and ``model``, are the arguments
# of the constructor of its class. You can check
# which arguments a class accepts, and therefore which fields you can write in a
# configuration file, with ``help()``:

help(type(quads[0]))

# %%
