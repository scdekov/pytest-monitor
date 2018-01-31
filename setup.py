#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from io import open

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('pytest_monitor')


setup(
    name='pytest-monitor',
    version=version,
    url='https://git@github.com/scdekov/pytest-monitor.git',
    description='Run pytest on project file modification and notify you.',
    packages=get_packages('pyetst-monitor'),
    package_data=get_package_data('pyetst-monitor'),
    install_requires=[
        'notify2==0.3.1',
        'watchdog==0.8.3'
    ],
    entry_points={
        'console_scripts': [
            'pytest-monitor = pytest-monitor.pytest-monitor:main'
        ]
    },
)
