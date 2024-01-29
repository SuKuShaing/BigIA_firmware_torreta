from setuptools import setup
from Cython.Build import cythonize

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
    name='motores',
    ext_modules=cythonize("motores.pyx", annotate=True, compiler_directives={'language_level' : "3"}),
)