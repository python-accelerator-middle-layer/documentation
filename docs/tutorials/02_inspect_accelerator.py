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
# Inspect the Accelerator Contents
# ------------------------------------
#
# The yellow pages provide an overview of the accelerator.
# This shows what is configured and available for use.

accelerator.yellow_pages

# %%
# Show the Configuration of an Array
# ------------------------------------

quads = accelerator.design.magnets.get("QForTune")
print(quads)

# %%
# Show the Configuration of an Magnet in Array
# --------------------------------------------

print(quads[0])

# %%
