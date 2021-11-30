#!/usr/bin/env python
# coding: utf-8
from pathlib import Path

from setuptools import find_packages, setup

ROOT_DIR = Path(__file__).resolve().parent

with open(ROOT_DIR / "README.md", "r", encoding="utf-8") as fh:
    README = fh.read()

with open(ROOT_DIR / "requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="aoc_utils",
    version="0.1.0",
    license="GNU General Public License (GNU GPL v3 or above)",
    author="Steven van de Graaf",
    author_email="steven@vandegraaf.xyz",
    description="A python package and CLI tool for Advent of Code",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="aoc advent of code utils cli",
    url="https://github.com/sgraaf/Advent-of-Code-Utils",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={"console_scripts": ["aocli = aoc_utils.cli:app"]},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
    ],
)
