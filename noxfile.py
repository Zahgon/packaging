# /// script
# dependencies = ["nox>=2025.02.09", "packaging"]
# ///

from __future__ import annotations

import contextlib
import datetime
import difflib
import glob
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import textwrap
import time
import urllib.request
from pathlib import Path
from typing import IO, Generator

import nox

import packaging.version  # will always be present with nox

nox.needs_version = ">=2025.02.09"
nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "uv|virtualenv"

PYPROJECT = nox.project.load_toml("pyproject.toml")
PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT)


@nox.session(
    python=[
        *PYTHON_VERSIONS,
        "3.13t",
        "3.14t",
        "pypy3.8",
        "pypy3.9",
        "pypy3.10",
        "pypy3.11",
    ],
    default=False,
)
def tests(session: nox.Session) -> None:
    """
    Run the tests, with coverage.
    """
    pass


@nox.session(default=False)
def property_tests(session: nox.Session) -> None:
    """
    Run property-based tests (no coverage).
    """
    pass


PROJECTS = {
    "packaging_legacy": "https://github.com/di/packaging_legacy/archive/refs/tags/23.0.post0.tar.gz",
    "build": "https://github.com/pypa/build/archive/refs/tags/1.4.0.tar.gz",
    "setuptools": "https://github.com/pypa/setuptools/archive/refs/tags/v82.0.0.tar.gz",
    "pyproject_metadata": "https://github.com/pypa/pyproject-metadata/archive/refs/tags/0.11.0.tar.gz",
    "pip": "https://github.com/pypa/pip/archive/refs/tags/26.0.1.tar.gz",
}


@nox.parametrize("project", list(PROJECTS))
@nox.session(default=False)
def downstream(session: nox.Session, project: str) -> None:
    """
    Run downstream projects with this packaging.
    """
    pass


@nox.session(python="3.10")
def lint(session: nox.Session) -> None:
    """
    Run the linters.
    """
    pass


@nox.session(default=False)
def docs(session: nox.Session) -> None:
    """
    Build the docs.
    """
    pass


@nox.session(default=False)
def release(session: nox.Session) -> None:
    """
    Give a version number to use as tag.
    """
    pass


@nox.session
def release_build(session: nox.Session) -> None:
    """
    Build version from command-line arguments otherwise current Git tag.
    """
    pass


@nox.session(default=False)
def update_licenses(session: nox.Session) -> None:
    """
    Update licenses.
    """
    pass


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _build_and_check(
    session: nox.Session,
    release_version: str,
    remove: bool = False,
) -> None:
    pass


def _get_version_from_arguments(arguments: list[str]) -> str:
    """Checks the arguments passed to `nox -s release`.

    Only 1 argument that looks like a version? Return the argument.
    Otherwise, raise a ValueError describing what's wrong.
    """
    pass


def _check_working_directory_state(session: nox.Session) -> None:
    """Check state of the working directory, prior to making the release."""
    pass


def _check_git_state(session: nox.Session, version_tag: str) -> None:
    """Check state of the git repository, prior to making the release."""
    pass


def _bump(session: nox.Session, *, version: str, file: Path, kind: str) -> None:
    pass


@contextlib.contextmanager
def _replace_file(
    original_path: Path,
) -> Generator[tuple[IO[str], IO[str]], None, None]:
    # Create a temporary file.
    pass


def _changelog_update_unreleased_title(version: str, *, file: Path) -> None:
    """Update an "*unreleased*" heading to "{version} - {date}" """
    pass


def _changelog_add_unreleased_title(*, file: Path) -> None:
    pass


if __name__ == "__main__":
    nox.main()
