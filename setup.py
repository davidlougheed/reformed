#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="reformed",
    version="0.1.0",

    python_requires="~=3.8",
    install_requires=[
        "tornado>=6.2,<6.3",
    ],

    description="Document format conversion service based on Pandoc.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/davidlougheed/reformed",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

    author="David Lougheed",
    author_email="david.lougheed@gmail.com",

    packages=find_packages(exclude="tests"),
)
