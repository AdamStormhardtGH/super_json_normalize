#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Adam Rudd",
    author_email='Adam@adamrudd.net',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A generic, unlimited level json normalizer which handles arrays at any location. Outputs a normalised set of data which can be imported into a relational table, and pulls in parent keys for joinability",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='super_json_normalize',
    name='super_json_normalize',
    packages=find_packages(include=['super_json_normalize', 'super_json_normalize.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AdamRuddGH/super_json_normalize',
    version='0.1.0',
    zip_safe=False,
)
