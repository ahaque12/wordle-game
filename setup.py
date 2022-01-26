from Cython.Build import cythonize
from distutils.core import setup

setup(
    name='Wordle Game',
    ext_modules = cythonize("helper.pyx")
)