from __future__ import annotations

import collections
import contextlib
import functools
import os
import re
import sys
import warnings
from typing import Generator, Iterator, NamedTuple, Sequence

from ._elffile import EIClass, EIData, ELFFile, EMachine

EF_ARM_ABIMASK = 0xFF000000
EF_ARM_ABI_VER5 = 0x05000000
EF_ARM_ABI_FLOAT_HARD = 0x00000400

_ALLOWED_ARCHS = {
    "x86_64",
    "aarch64",
    "ppc64",
    "ppc64le",
    "s390x",
    "loongarch64",
    "riscv64",
}


# `os.PathLike` not a generic type until Python 3.9, so sticking with `str`
# as the type for `path` until then.
@contextlib.contextmanager
def _parse_elf(path: str) -> Generator[ELFFile | None, None, None]:
    pass


def _is_linux_armhf(executable: str) -> bool:
    # hard-float ABI can be detected from the ELF header of the running
    # process
    # https://static.docs.arm.com/ihi0044/g/aaelf32.pdf
    pass


def _is_linux_i686(executable: str) -> bool:
    pass


def _have_compatible_abi(executable: str, archs: Sequence[str]) -> bool:
    pass


# If glibc ever changes its major version, we need to know what the last
# minor version was, so we can build the complete list of all versions.
# For now, guess what the highest minor version might be, assume it will
# be 50 for testing. Once this actually happens, update the dictionary
# with the actual value.
_LAST_GLIBC_MINOR: dict[int, int] = collections.defaultdict(lambda: 50)


class _GLibCVersion(NamedTuple):
    major: int
    minor: int


def _glibc_version_string_confstr() -> str | None:
    """
    Primary implementation of glibc_version_string using os.confstr.
    """
    pass


def _glibc_version_string_ctypes() -> str | None:
    """
    Fallback implementation of glibc_version_string using ctypes.
    """
    pass


def _glibc_version_string() -> str | None:
    """Returns glibc version string, or None if not using glibc."""
    pass


def _parse_glibc_version(version_str: str) -> _GLibCVersion:
    """Parse glibc version.

    We use a regexp instead of str.split because we want to discard any
    random junk that might come after the minor version -- this might happen
    in patched/forked versions of glibc (e.g. Linaro's version of glibc
    uses version strings like "2.20-2014.11"). See gh-3588.
    """
    pass


@functools.lru_cache
def _get_glibc_version() -> _GLibCVersion:
    pass


# From PEP 513, PEP 600
def _is_compatible(arch: str, version: _GLibCVersion) -> bool:
    pass


_LEGACY_MANYLINUX_MAP: dict[_GLibCVersion, str] = {
    # CentOS 7 w/ glibc 2.17 (PEP 599)
    _GLibCVersion(2, 17): "manylinux2014",
    # CentOS 6 w/ glibc 2.12 (PEP 571)
    _GLibCVersion(2, 12): "manylinux2010",
    # CentOS 5 w/ glibc 2.5 (PEP 513)
    _GLibCVersion(2, 5): "manylinux1",
}


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate manylinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be manylinux-compatible.

    :returns: An iterator of compatible manylinux tags.
    """
    pass
