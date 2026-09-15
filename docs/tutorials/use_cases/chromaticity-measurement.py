#!/usr/bin/env python
# coding: utf-8
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
"""Chromaticity Measurement
============================

This tutorial shows how to measure the chromaticity.
"""

# %%
# Prerequisites
# -------------
#
# The tutorial requires an existing pyAML configuration file which includes configuration
# of the chromaticity monitor.
#
# The example uses the configuration provided by the ``pyaml-test-lattice`` package.

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
# Momentum Compaction Factor
# --------------------------
#
# The momentum compaction factor is needed to convert RF frequency deviation to
# momentum deviation. It is computed from the lattice model (design mode).

accelerator.design.get_lattice().disable_6d()
alphac = accelerator.design.get_lattice().get_mcf()
accelerator.design.get_lattice().enable_6d()
print(f"Momentum compaction factor: αc = {alphac:.6e}")

# %%
# Chromaticity Measurement
# ------------------------
#
# The chromaticity monitor is named `CHROMATICITY_MONITOR` in the configuration.
# The measurement sweeps the RF frequency and fits the resulting tune shift.
#
# Parameters:
#
# - ``alphac`` — momentum compaction factor (from lattice above)
# - ``fit_order`` — polynomial fit order (2 = quadratic)
# - ``n_step`` — number of RF frequency steps
# - ``sleep_between_meas`` / ``sleep_between_step`` — settling times (set to ``wait_time`` for live mode)
# - ``do_plot=True`` — show the tune vs. δp fit

def chroma_callback(action: int, cb_data: dict):
    if action == Action.MEASURE:
        print(f"Chromaticity: #{cb_data['step']} RF={cb_data['rf']:.2f} Hz, Tune={cb_data['tune']}")
    return True

# %%
chroma_monitor = SR.get_chromaticity_monitor("CHROMATICITY_MONITOR")

# Measure the chromaticity
chroma_monitor.measure(
    callback=chroma_callback,
    do_plot=True,
    alphac=alphac,
    fit_order=2,
    n_step=5,
    sleep_between_meas=wait_time,
    sleep_between_step=wait_time,
)

# Get the measured chromaticity
ksi = chroma_monitor.chromaticity.get()
print(f"Measured chromaticity: ξx = {ksi[0]:.3f}, ξy = {ksi[1]:.3f}")

