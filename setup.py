from setuptools import setup
from Cython.Build import cythonize
from sage.env import sage_include_directories

setup(
    ext_modules=cythonize(
        ["cycles.pyx", "k_shortest.pyx"],
        include_path=sage_include_directories(),
        compiler_directives={'language_level': 3}
    )
)