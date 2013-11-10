from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "CiteNet",
    version = "0.0.1",
    packages = find_packages(),
    scripts = ['scripts/citenet'],
    
    install_requires = """
      networkx>=1.8.1
      scipy>=0.9.0
    """,

    author = "Ben Pringle",
    author_email = "ben.pringle@gmail.com",
    description = "Citation network analysis package",
    license = "MIT",
)
