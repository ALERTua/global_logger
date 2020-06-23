#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pendulum==2.0.3', 'pathlib', 'colorama', 'colorlog']

setup_requirements = requirements

test_requirements = requirements

setup(
    author="Alexey Rubasheff",
    author_email='alexey.rubasheff@gmail.com',
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3.8',
    ],
    description="Flexible Python Logger",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='python_flexible_logger',
    name='python_flexible_logger',
    packages=find_packages(include=['python_flexible_logger', 'python_flexible_logger.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/alertua/python_flexible_logger',
    version='0.1.0',
    zip_safe=False,
)
