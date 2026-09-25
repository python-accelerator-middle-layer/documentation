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

This tutorial shows how to find out what an accelerator contains using the *yellow pages*,
and how to access what you found.

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
# The Yellow Pages
# ----------------
#
# The yellow pages are a directory of everything the accelerator provides: the control modes
# and, sorted by category, the arrays, the tuning tools and the diagnostics. They are built
# automatically by scanning every control mode, so they always reflect what is configured.
#
# Printing them gives an overview:

yp = accelerator.yellow_pages
print(yp)

# %%
# Categories and Entries
# ~~~~~~~~~~~~~~~~~~~~~~
# The entries are sorted in categories. ``keys()`` lists the entries of one category, or of
# all categories if none is given.

print(yp.categories())
print("Arrays:     ", yp.keys("Arrays"))
print("Tools:      ", yp.keys("Tools"))
print("Diagnostics:", yp.keys("Diagnostics"))

# %%
# Check an Entry
# ~~~~~~~~~~~~~~
# ``has()`` tells whether an entry exists, and ``availability()`` in which control modes it
# can be used.

print(yp.has("QForTune"), yp.has("QF"))
print(yp.availability("DEFAULT_TUNE_CORRECTION"))

# %%
# Get an Object
# ~~~~~~~~~~~~~
# An entry can be accessed as an attribute of the yellow pages. The result gives the object
# in each control mode where it is available.

qfortune = yp.QForTune
print(qfortune.keys())

# %%
# The object of a given mode is the same as the one reached through the control mode itself:

print(qfortune["design"] is accelerator.design.magnets.get("QForTune"))

# %%
# Search Element Names
# ~~~~~~~~~~~~~~~~~~~~
# Indexing the yellow pages searches the names of the elements. With the name of an array,
# it returns the names of the elements of the array:

print(yp["Cell1"])

# %%
# Wildcards can be used to match several names:

print(yp["QF_00*"])

# %%
# For more complex searches, use a regular expression by starting the query with ``re:``:

print(yp["re:^(QF|QD)_01[0-2]$"])

# %%
# ``get()`` does the same search and can be restricted to one control mode. Here the
# correctors ``COR_00x`` are combined-function magnets: the search returns both the magnets and
# their horizontal (``.hcorrector``) and vertical (``.vcorrector``) parts, which are the
# elements of the ``HCorr`` and ``VCorr`` arrays.

print(yp.get("COR_00*", mode="design"))

# %%
# Use the Result
# ~~~~~~~~~~~~~~
# The names returned by a search can be used to access the elements in any control mode:

for name in yp["re:^QF_00[1-3]$"]:
    magnet = accelerator.design.magnet.get(name)
    print(name, magnet.strength.get())

# %%
