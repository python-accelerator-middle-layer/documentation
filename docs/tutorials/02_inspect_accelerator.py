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
# Show the Configuration of a Magnet
# ------------------------------------

accelerator.design.magnets.get("QF_001")
