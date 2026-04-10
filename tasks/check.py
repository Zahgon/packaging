# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import contextlib
import itertools
import json
import os.path
import xmlrpc.client

import invoke
import pkg_resources
import progress.bar

from packaging.version import Version

from .paths import CACHE


def _parse_version(value: str) -> Version | None:
    pass


@invoke.task
def pep440(cached: bool = False) -> None:
    pass
