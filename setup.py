from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("k_shortest.pyx", language_level="3")
)