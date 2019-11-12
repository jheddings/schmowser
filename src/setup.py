# py2app setup file for schmowser

from setuptools import setup

# this is expecting to run from the base directory of the project

setup(
    name='Schmowser',
    description='Utility for redirecting links to a user-specified browser...  a.k.a browser-shmowser',
    url='https://github.com/jheddings/schmowser',
    license='MIT',
    app=['src/schmowser.py'],
    setup_requires=['py2app'],
)
