# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

from setuptools import setup, find_packages
from .nbi_extension_example._version import __version__

setup(
    name='nbi_example_extension',
    version=__version__,
    packages=find_packages(),
    include_package_data=True
)
