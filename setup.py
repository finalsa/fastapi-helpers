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
    python_requires=">=3.8",
    data_files=[("", ["LICENSE.md"])],
    install_requires=[
        "argon2-cffi>=23.1.0",
        "aiosqlite>=0.19.0",
        "ormar>=0.12.2",
        'pydantic>=1.10.8',
        "fastapi>=0.105.0",
        "fastapi-better-logger>=0.0.5",
        "typing_extensions>=4.9.0",
        "watchtower>=3.0.0",
        "boto3>=1.20.3"
    ],
    extras_require={
        "postgresql": ["asyncpg", "psycopg2-binary"],
        "mysql": ["aiomysql", "pymysql"],
        "sqlite": ["aiosqlite"],
        "orjson": ["orjson"],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
