#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup

PACKAGE = "fastapi_helpers"
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
    zip_safe=True,
    python_requires=">=3.7",
    data_files=[("", ["LICENSE.md"])],
    install_requires=[
        "aiosqlite>=0.17.0",
        "argon2-cffi>=21.3.0",
        "ormar>=0.10.24",
        'pydantic>=1.8.2',
        "fastapi>=0.70.0",
        "typing_extensions>=3.7,<3.10.0.3",
        "watchtower>=2.0.1",
        "boto3>=1.20.3"
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
