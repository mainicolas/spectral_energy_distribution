from setuptools import Extension, setup
from Cython.Build import cythonize

ext = Extension("interface", sources=["interface.pyx", "c_astrom2.c"])

setup(ext_modules=cythonize(ext,compiler_directives={'language_level' : "3"}))