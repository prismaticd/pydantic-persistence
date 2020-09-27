"""Sphinx configuration."""
from datetime import datetime

project = "Prismatic Package"
author = "Prismatic"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
html_static_path = ["_static"]
