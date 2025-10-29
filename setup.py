from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ["cycles.pyx", "k_shortest.pyx"],
        compiler_directives={'language_level': 3}
    )
)