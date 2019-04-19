#!/usr/bin/env python

# Copyright (C) 2019  Cooper Yang <cm_yang@yeah.net>
#
# This file is part of pyNfsClient.
#
# NfsClient is free software; you can redistribute it and/or modify it under the
# terms of the MIT License.
#
# NfsClient is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the MIT License for more details.

import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = dict()
with open(os.path.join(here, "pyNfsClient", "__info__.py"), "r") as fp:
    exec(fp.read(), about)

with open("README.rst", encoding="utf-8") as f:
    readme = f.read()

with open("HISTORY.md", encoding="utf-8") as f:
    history = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type='text/x-rst',
    author=about["__author__"],
    author_email=about["__author_email__"],
    license="MIT",
    platforms='any',
    url=about["__url__"],
    packages=["pyNfsClient"],
    python_requires=">=2.7",
    keywords="RPC NFS struct",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Filesystems',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
