"""
Test page
=================

This is a minimal Sphinx-Gallery example you can use to verify that:

- the page is picked up by Sphinx-Gallery
- code cells are executed
- plots are rendered
- the Binder button appears on the generated page
"""

# %%
# Imports
# -------

import numpy as np
import matplotlib.pyplot as plt

# %%
# Create some data
# ----------------

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

# %%
# Plot the data
# -------------

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, label="sin(x)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Sphinx-Gallery test plot")
ax.grid(True)
ax.legend()

plt.show()

# %%
# A second cell
# -------------

x2 = np.linspace(0, 2 * np.pi, 30)
y2 = np.cos(x2)

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(x2, y2, label="cos(x)", marker="o")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Second plot")
ax.grid(True)
ax.legend()

plt.show()