# -*- coding: utf-8 -*-
"""Package for implementing a RPi lock client"""
from setuptools import setup

setup(
    name="RPi lock client",
    description="Package for Secured Pi locks",
    version="0.1.0",
    author="Steven Than, David Smiths, Tatiana Weaver, Crystal Lessor",
    author_email="",
    license="MIT",
    py_modules=["RPi-client"],
    package_dir={'': 'src'},
   # install_requires=['socketIO_client','SPI-Py','MFRC522'],
   install_requires=['socketIO_client'],
    extras_require={'test': ['pytest', 'pytest-watch', 'tox']},
)
