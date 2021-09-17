#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup

PACKAGE = "fastapiutils"
URL = "https://github.com/finalsa/fastapi-utils"


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name=PACKAGE,
    version=get_version(PACKAGE),
    url=URL,
    license="MIT",
    description="An utils package for fastapi",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords=[
        "fastapi",
        "sqlalchemy",
        "ormar",
        "pydantic",
    ],
    author="Luis Jimenez",
    author_email="luis@finalsa.com",
    packages=get_packages(PACKAGE),
    package_data={PACKAGE: ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    data_files=[("", ["LICENSE.md"])],
    install_requires=[
        "ormar>=0.3.2,<0.5.2",
        "pydantic>=1.6.1,!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<=1.8.2",
        "fastapi>=0.67.0,<=0.68.1",
        "typing_extensions>=3.7,<3.10.0.3",
    ],
    extras_require={
        "postgresql": ["asyncpg", "psycopg2-binary"],
        "mysql": ["aiomysql", "pymysql"],
        "sqlite": ["aiosqlite"],
        "orjson": ["orjson"],
        "crypto": ["cryptography"],
    },
    classifiers=[
    ],
)
