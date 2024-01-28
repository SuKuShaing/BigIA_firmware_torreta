from setuptools import setup
from Cython.Build import cythonize

setup(
    name='motores',
    ext_modules=cythonize("motores.pyx"),
)