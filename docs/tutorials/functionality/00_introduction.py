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
Introduction to pyAML
==========================================================

This tutorial is the starting point of the pyAML tutorials. It introduces what pyAML is,
the main concepts you will meet in the other tutorials, and how the tutorials are organized.
It does not contain any code: the hands-on part starts in the next tutorial.
"""

# %%
# What is pyAML?
# --------------
#
# The Python Accelerator Middle Layer (pyAML) is a Python library, developed by a
# collaboration of accelerator facilities, that gives a common, physics-oriented way to
# access a particle accelerator. With pyAML you read "the orbit at all BPMs" or set
# "the strength of quadrupole QF_001" without having to know which control system variable
# holds the value, or how a power-supply current is converted into a magnetic strength.
#
# Its main goals are to:
#
# - provide the same interface for the real machine, a virtual accelerator and a simulation
#   model, independently of the control system (TANGO, EPICS, ...),
# - allow measurement and correction tools (orbit, tune, chromaticity, ...) to be written
#   once and shared between facilities,
# - allow those tools to be developed and tested on a simulation, without using beam time.
#
# You can read more about the motivation and goals in
# :doc:`What is pyAML? <../../explanation/about>`.

# %%
# Main Concepts
# -------------
#
# Working with pyAML means working with a small hierarchy of objects:
#
# .. figure:: /_static/pyaml-hierarchy.svg
#    :alt: Hierarchy of pyAML objects
#    :width: 100%
#
# - **Accelerator**: the top-level object describing one machine. It is created from a
#   configuration.
# - **Control mode**: one way of accessing the accelerator. ``accelerator.live`` talks to the
#   control system (the real machine or a virtual accelerator), ``accelerator.design`` talks
#   to a simulation of the machine made with `pyAT <https://atcollab.github.io/at/p/index.html>`_.
#   Both provide exactly the same interface.
# - **Element**: one object of the machine, such as a magnet, a BPM or the RF plant.
# - **Array**: a named group of elements which can be read or set in one call, such as all
#   the BPMs.
# - **Attribute**: a value of an element that can be read with ``get()`` and written
#   with ``set()``, such as the ``strength`` of a magnet.
# - **Configuration**: a YAML or JSON file describing all of the above. Each item of the
#   configuration names a Python class with its ``class`` field, and **each other field is an
#   argument of that class's constructor**. This rule is explored in the first tutorial.
#
# See :doc:`pyAML Structure <../../explanation/architecture>` and
# :doc:`Control Modes <../../explanation/control-modes>` for more details.

# %%
# How the Tutorials Work
# ----------------------
#
# **Running the tutorials.** Each tutorial can be run in the cloud with
# `Binder <https://mybinder.org>`_ using the launcher on its page, with nothing to install,
# or downloaded and run on your own computer, as a Jupyter notebook or a Python script
# (see below).
#
# **The test machine.** The tutorials use a small test storage ring, with its lattice and
# ready-made pyAML configurations, provided by the ``pyaml-test-lattice`` package. It is
# presented in the tutorials where it is first used.
#
# **The control mode.** The tutorials use the ``design`` control mode, a simulation of the
# machine, so no control system is needed. To run them on the ``live`` control mode, you need a
# control system, for example a virtual accelerator of the test machine
# (see :doc:`Installing Apptainer <../../how-to/virtual-accelerator/apptainer>`).
# Since all control modes have the same interface, switching is a single line:
#
# .. code-block:: python
#
#    SR = accelerator.design   # replace by accelerator.live to use the control system

# %%
# Run the Tutorials Locally
# -------------------------
#
# You need Python 3.11 or newer. Always install in a virtual environment, to avoid breaking
# your Python installation (see :doc:`New to Python <../../how-to/getting-started/python-basics>`
# if you are not familiar with virtual environments). Then install:
#
# .. code-block:: bash
#
#    pip install "accelerator-middle-layer[cs-oa-tango]" pyaml-test-lattice jupyterlab
#
# This installs:
#
# - ``accelerator-middle-layer``: the ``pyaml`` core package. It also installs pyAT, used by
#   the ``design`` control mode, together with numpy and matplotlib.
# - ``[cs-oa-tango]``: the ``pyaml-cs-oa`` control-system bindings for TANGO. The ready-made
#   configurations of the test machine declare a ``live`` control mode using these bindings,
#   so they are needed to load them, even if you only use the ``design`` control mode.
# - ``pyaml-test-lattice``: the test machine, with its lattice and pyAML configurations.
# - ``jupyterlab``: to open the tutorials as notebooks. It is not needed to run them as
#   Python scripts.
#
# The other control-system bindings (``cs-oa-epics``, ``tango-pyaml``) are only needed to
# connect to your own control system, see
# :doc:`User Installation <../../how-to/installation/user-installation>`. To get exactly the
# same environment as on Binder, install the
# `Binder requirements <https://github.com/python-accelerator-middle-layer/documentation/blob/main/binder/requirements.txt>`_
# instead: ``pip install -r binder/requirements.txt`` from a clone of the documentation
# repository.
#
# Finally, download a tutorial as a notebook or a Python script with the download links in
# the right sidebar of its page, and run it with ``jupyter lab`` or ``python``.

# %%
# Where to Go Next
# ----------------
#
# The tutorials are designed to be followed in this order:
#
# 1. :doc:`Create an Accelerator <01_create_accelerator>`: create an accelerator
#    interactively and from a configuration file, and learn how the configuration maps to
#    Python classes.
# 2. :doc:`Inspect an Accelerator <02_inspect_accelerator>`: explore what a complete
#    accelerator configuration contains.
# 3. The **use cases**, which apply pyAML to real tasks:
#    :doc:`tune correction <../use_cases/tune-correction>`,
#    :doc:`orbit correction <../use_cases/orbit_correction>` and
#    :doc:`chromaticity measurement <../use_cases/chromaticity-measurement>`.
#
# For more background, read the explanations:
# :doc:`What is pyAML? <../../explanation/about>`,
# :doc:`pyAML Structure <../../explanation/architecture>`,
# :doc:`Control Modes <../../explanation/control-modes>` and
# :doc:`Configuration Structure and Syntax <../../explanation/configuration>`.

# sphinx_gallery_thumbnail_path = '_static/pyaml-hierarchy.svg'
