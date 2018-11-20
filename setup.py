"""Packaging configuration."""
import os

from setuptools import setup, find_packages

with open(os.path.abspath('VERSION.txt'), 'r') as fd:
    VERSION = fd.read().strip()

setup(
    name='aws-cloudformation-utils',
    version=VERSION,
    description='Collections of utility functions for Troposphere/CloudFormation.',
    url='',
    author='VRT DPC',
    author_email='dpc@vrt.be',
    license='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cloudformation aws',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    data_files=['VERSION.txt'],
    install_requires=[
    ],
)
