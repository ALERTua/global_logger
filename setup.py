#!/usr/bin/env python

"""The setup script."""
import os
# noinspection PyProtectedMember,PyCompatibility
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

cur_file_dir_path = os.path.dirname(os.path.abspath(__file__))

# noinspection PyTypeChecker
install_reqs = parse_requirements(os.path.join(cur_file_dir_path, 'global_logger/requirements.txt'), session='hack')
reqs = [r.requirement for r in install_reqs]

requirements = reqs
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Global Logger",
    install_requires=requirements,
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
    version='0.1.0',
    zip_safe=False,
)
