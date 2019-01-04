from distutils.core import setup
from Cython.Build import cythonize

import os

setup(
    ext_modules=cythonize(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'percent_white_pixels.pyx'
        )
    )
)
