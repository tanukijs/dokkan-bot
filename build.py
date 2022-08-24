from distutils.core  import Extension, setup
from Cython.Build import cythonize

ext = Extension(name="cli", sources=["./src/cli.py"])
setup(ext_modules=cythonize(ext))