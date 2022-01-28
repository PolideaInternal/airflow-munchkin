#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "apache-airflow==2.2.0",
    "Click>=6.0",
    "google-cloud-automl==0.4.0",
    "google-cloud-redis==0.2.1",
    "tzlocal<2.0.0.0,>=1.5.0.0",
]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Polidea",
    author_email="hello@polidea.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={"console_scripts": ["airflow_munchkin=airflow_munchkin.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="airflow_munchkin",
    name="airflow_munchkin",
    packages=find_packages(include=["airflow_munchkin"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/PolideaInternal/airflow_munchkin",
    version="0.1.0",
    zip_safe=False,
)
