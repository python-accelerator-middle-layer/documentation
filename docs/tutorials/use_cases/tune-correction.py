# -*- coding: utf-8 -*-
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
"""Tune Correction
=================

This tutorial shows how to read and correct the betatron tunes.
"""

# %%
# Prerequisites
# -------------
#
# The tutorial requires an existing pyAML configuration file which includes configuration
# of the tune monitor and tune correction.
#
# The example uses the configuration provided by the ``pyaml-test-lattice`` package.

# Get the path to the configuration file
# sphinx_gallery_thumbnail_path = '_static/tune_correction.svg'

from pyaml.common.constants import Action
from pyaml_test_lattice import configurations

# %%
# Load the Accelerator
# --------------------

from pyaml.accelerator import Accelerator
accelerator = Accelerator.load(configurations["pyaml/tango/pyaml-cs-oa/fodo_1gev_6d_pyaml-oa.yaml"])

# Print the string representation of the accelerator
print(accelerator)

# %%
# Control Mode Choice
# --------------------
#
# - ``accelerator.design`` — runs pyAT locally, no control system needed. Set ``wait_time = 0.0``.
# - ``accelerator.live`` — connects to the real machine or virtual twin. Set ``wait_time`` to allow readback settling (typically 1.5–2 s).
#
# For ``live`` control mode you need a running control system or virtual accelerator.
# If you want to skip this, run the notebook in `design`` mode only.

# Use the design mode
SR = accelerator.design

# For live mode
# SR = accelerator.live

wait_time = 0.0 if SR == accelerator.design else 2.0

# Print the string representation of the simulator
print(SR)

# %%
# Betatron Tune Monitor
# -----------------------
#
# The tune monitor is defined in the configuration file under the name `BETATRON_TUNE`.

# %%
tune_monitor = SR.get_betatron_tune_monitor("BETATRON_TUNE")

# Print the string representation of the tune monitor
print(tune_monitor)

print(f"Current tune: {tune_monitor.tune.get()}")


# %%
# Quadrupolar Correctors
# ----------------------
#
# The `QForTune` array contains the quadrupoles used for tune correction.
# You can access and set strengths of individual correctors.


# %%
qcorrectors = SR.magnets.get("QForTune")
first_q = qcorrectors[0]

print(f"The ring has {len(qcorrectors)} quadrupolar correctors. First corrector: {first_q.get_name()}")

# Print the string representation of the first quadrupole
print(qcorrectors[0])

# Get the current strength
str_before = qcorrectors[0].strength.get()
print(f"Current strength: {qcorrectors[0].strength.get()=:.4f}")

# Set the strength
qcorrectors[0].strength.set(str_before + 0.002)
print(f"After stepping by 0.002: {qcorrectors[0].strength.get()=:.4f}")

# Reset the strength
qcorrectors[0].strength.set(str_before)
print(f"Reset to {str_before:.4f}")

# %%
# Tune Correction
# -----------------------------
#
# ``SR.tune`` is the `DEFAULT_TUNE_CORRECTION` tool. ``SR.trm`` is the `DEFAULT_TUNE_RESPONSE_MATRIX` tool.
#
# Before correcting the tune you need a response matrix. It can be measured as shown below or loaded from a previously saved file.

# Print the string representation of the tune correction tool
SR.tune

# %%
# Measure the Tune Response Matrix
# ---------------------------------
#
# The callback below prints progress during the measurement. The ``sleep_between_step``` parameter controls the wait time between corrector steps — set it to 0 for design mode.
#
# **Note:** on some lattices ``disable_6d()`` is required before measuring in design mode since it only works in 4D.

# Required on some lattices before measuring the TRM in design mode
accelerator.design.get_lattice().disable_6d()

def tune_callback(action: int, cb_data: dict):
    if action == Action.MEASURE:
        print(f"Tune response: #{cb_data['step']} {cb_data['magnet']} {cb_data['tune']}")
    return True

# Measure the response matrix
SR.trm.measure(sleep_between_step=wait_time, callback=tune_callback)
SR.trm.save("trm.json")

# Load the measured response matrix
SR.tune.load("trm.json")
print("Response matrix loaded.")

# Print string representation of the tune response matrix
print(SR.trm)

# %%
# Correcting the tune
# -----------------------------
#
# ``SR.tune.set([qx, qy])`` runs the correction iteratively.
# The ``iter`` parameter controls the number of iterations and ``wait_time`` the settling time between each iteration.

# %%
print(f"Tune before correction: {SR.tune.readback()}")

qx, qy = 0.19, 0.28
print(f"\nSetting tune to [{qx}, {qy}]")
SR.tune.set([qx, qy], iter=10, wait_time=wait_time)
print(f"Tune after correction: {SR.tune.readback()}")

qx, qy = 0.21, 0.30
print(f"\nSetting tune to [{qx}, {qy}]")
SR.tune.set([qx, qy], iter=10, wait_time=wait_time)
print(f"Tune after correction: {SR.tune.readback()}")

# Print the string representation of the tune correction
SR.tune
