# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyAML Documentation'
copyright = '2026, pyAML Collaboration'
author = 'pyAML Collaboration'
release = ''

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton",
    "myst_nb",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
]

templates_path = ['_templates']
exclude_patterns = []

sd_fontawesome_source = "cdn"

myst_enable_extensions = [
    "attrs_inline",
]

sphinx_gallery_conf = {
    "examples_dirs": "tutorials_src",
    "gallery_dirs": "tutorials",

    # Binder (cloud notebook)
    "binder": {
        "org": "python-accelerator-middle-layer",
        "repo": "documentation",
        "branch": "main",
        "binderhub_url": "https://mybinder.org",
        "dependencies": ["../../requirements.txt"],
        "use_jupyter_lab": True,
    },
}

exclude_patterns += [
    "tutorials/*.ipynb",
    "tutorials/*.py",
    "tutorials/*.zip",
    "tutorials/*.codeobj.json",
    "tutorials_src/GALLERY_HEADER.rst"
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_title = "pyAML Documentation"
html_show_sourcelink = False
html_logo = "_static/_images/logo.png"
html_css_files = ["custom.css"]
html_sidebars = {
    "reference/index": [],
}
html_theme_options = {
    "secondary_sidebar_items": ["page-toc","sg_download_links", "sg_launcher_links"],
}
