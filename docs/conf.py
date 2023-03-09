"""Sphinx configuration."""
project = "Appgen"
author = "Nyimbi Odero"
copyright = "2022, Nyimbi Odero"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
