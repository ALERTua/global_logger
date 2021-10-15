#!/usr/bin/env python

"""The setup script."""
import os

# noinspection PyProtectedMember,PyCompatibility
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

cur_file_dir_path = os.path.dirname(os.path.abspath(__file__))

with open('global_logger/requirements.txt') as f:
    install_requirements = [
        line.strip()
        for line in f.readlines()
        if line.strip() and not line.startswith('#')
    ]

setup_requirements = []
test_requirements = [
    "setuptools",
    "pip",
    "wheel",
    "watchdog",
    "flake8",
    "tox",
    "coverage",
    "Sphinx",
    "twine",
    "pendulum==2.0.3; python_version < '3'",  # fixed version
    "pendulum; python_version >= '3'",  # fixed version
    "pathlib",
    "colorama",
    "colorlog",
    "future",
    "zipp",
    "pytest",
    "enum; python_version < '3'",
]

setup(
    author="Alexey Rubasheff",
    author_email='alexey.rubasheff@gmail.com',
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="Based on Python built-in logger, expands it, and provides a global logger to your system. "
                "Easy on-screen and/or .log files output setup without pain for Python newcomers. "
                "Python 2 and 3 compatible",
    install_requires=install_requirements,
    license="MIT license",
    long_description='%s\n\n%s' % (readme, history),
    include_package_data=True,
    keywords='global_logger',
    name='global_logger',
    packages=find_packages(include=['global_logger', 'global_logger.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/alertua/global_logger',
    version='0.3.26',
    zip_safe=False,
)
