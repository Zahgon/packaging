# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import logging
import operator
import platform
import re
import struct
import subprocess
import sys
import sysconfig
from importlib.machinery import EXTENSION_SUFFIXES
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Iterator,
    Sequence,
    Tuple,
    TypeVar,
    cast,
)

from . import _manylinux, _musllinux

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import AbstractSet


__all__ = [
    "INTERPRETER_SHORT_NAMES",
    "AppleVersion",
    "PythonVersion",
    "Tag",
    "UnsortedTagsError",
    "android_platforms",
    "compatible_tags",
    "cpython_tags",
    "create_compatible_tags_selector",
    "generic_tags",
    "interpreter_name",
    "interpreter_version",
    "ios_platforms",
    "mac_platforms",
    "parse_tag",
    "platform_tags",
    "sys_tags",
]


def __dir__() -> list[str]:
    return __all__


logger = logging.getLogger(__name__)

PythonVersion = Sequence[int]
AppleVersion = Tuple[int, int]
_T = TypeVar("_T")

INTERPRETER_SHORT_NAMES: dict[str, str] = {
    "python": "py",  # Generic.
    "cpython": "cp",
    "pypy": "pp",
    "ironpython": "ip",
    "jython": "jy",
}


# This function can be unit tested without reloading the module
# (Unlike _32_BIT_INTERPRETER)
def _compute_32_bit_interpreter() -> bool:
    return struct.calcsize("P") == 4


_32_BIT_INTERPRETER = _compute_32_bit_interpreter()


class UnsortedTagsError(ValueError):
    """
    Raised when a tag component is not in sorted order per PEP 425.
    """


class Tag:
    """
    A representation of the tag triple for a wheel.

    Instances are considered immutable and thus are hashable. Equality checking
    is also supported.
    """

    __slots__ = ["_abi", "_hash", "_interpreter", "_platform"]

    def __init__(self, interpreter: str, abi: str, platform: str) -> None:
        """
        :param str interpreter: The interpreter name, e.g. ``"py"``
                                (see :attr:`INTERPRETER_SHORT_NAMES` for mapping
                                well-known interpreter names to their short names).
        :param str abi: The ABI that a wheel supports, e.g. ``"cp37m"``.
        :param str platform: The OS/platform the wheel supports,
                            e.g. ``"win_amd64"``.
        """
        self._interpreter = interpreter.lower()
        self._abi = abi.lower()
        self._platform = platform.lower()
        # The __hash__ of every single element in a Set[Tag] will be evaluated each time
        # that a set calls its `.disjoint()` method, which may be called hundreds of
        # times when scanning a page of links for packages with tags matching that
        # Set[Tag]. Pre-computing the value here produces significant speedups for
        # downstream consumers.
        self._hash = hash((self._interpreter, self._abi, self._platform))

    @property
    def interpreter(self) -> str:
        """
        The interpreter name, e.g. ``"py"`` (see
        :attr:`INTERPRETER_SHORT_NAMES` for mapping well-known interpreter
        names to their short names).
        """
        pass

    @property
    def abi(self) -> str:
        """
        The supported ABI.
        """
        pass

    @property
    def platform(self) -> str:
        """
        The OS/platform.
        """
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented

        return (
            (self._hash == other._hash)  # Short-circuit ASAP for perf reasons.
            and (self._platform == other._platform)
            and (self._abi == other._abi)
            and (self._interpreter == other._interpreter)
        )

    def __hash__(self) -> int:
        return self._hash

    def __str__(self) -> str:
        return f"{self._interpreter}-{self._abi}-{self._platform}"

    def __repr__(self) -> str:
        return f"<{self} @ {id(self)}>"

    def __setstate__(self, state: tuple[None, dict[str, Any]]) -> None:
        # The cached _hash is wrong when unpickling.
        _, slots = state
        for k, v in slots.items():
            setattr(self, k, v)
        self._hash = hash((self._interpreter, self._abi, self._platform))


def parse_tag(tag: str, *, validate_order: bool = False) -> frozenset[Tag]:
    """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of
    :class:`Tag` instances.

    Returning a set is required due to the possibility that the tag is a
    `compressed tag set`_, e.g. ``"py2.py3-none-any"`` which supports both
    Python 2 and Python 3.

    If **validate_order** is true, compressed tag set components are checked
    to be in sorted order as required by PEP 425.

    :param str tag: The tag to parse, e.g. ``"py3-none-any"``.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :raises UnsortedTagsError: If **validate_order** is true and any compressed tag
        set component is not in sorted order.

    .. versionadded:: 26.1
       The *validate_order* parameter.
    """
    pass


def _get_config_var(name: str, warn: bool = False) -> int | str | None:
    pass


def _normalize_string(string: str) -> str:
    pass


def _is_threaded_cpython(abis: list[str]) -> bool:
    """
    Determine if the ABI corresponds to a threaded (`--disable-gil`) build.

    The threaded builds are indicated by a "t" in the abiflags.
    """
    pass


def _abi3_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2. The free-threaded
    builds do not support abi3.
    """
    pass


def _abi3t_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3t.

    PEP 803 was first implemented in Python 3.15 but, per PEP 803, this
    returns tags going back to Python 3.2 to mirror the abi3
    implementation and leave open the possibility of abi3t wheels
    supporting older Python versions.

    """
    pass


def _cpython_abis(py_version: PythonVersion, warn: bool = False) -> list[str]:
    pass


def cpython_tags(
    python_version: PythonVersion | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for the CPython interpreter.

    The specific tags generated are:

    - ``cp<python_version>-<abi>-<platform>``
    - ``cp<python_version>-<stable_abi>-<platform>``
    - ``cp<python_version>-none-<platform>``
    - ``cp<older version>-<stable_abi>-<platform>`` where "older version" is all older
      minor versions down to Python 3.2 (when ``abi3`` was introduced)

    If ``python_version`` only provides a major-only version then only
    user-provided ABIs via ``abis`` and the ``none`` ABI will be used.

    The ``stable_abi`` will be either ``abi3`` or ``abi3t`` if `abi` is a
    GIL-enabled ABI like `"cp315"` or a free-threaded ABI like `"cp315t"`,
    respectively.

    :param Sequence python_version: A one- or two-item sequence representing the
                                 targeted Python version. Defaults to
                                 ``sys.version_info[:2]``.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    pass


def _generic_abi() -> list[str]:
    """
    Return the ABI tag based on EXT_SUFFIX.
    """
    pass


def generic_tags(
    interpreter: str | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter which requires no specialization.

    This function should be used if one of the other interpreter-specific
    functions provided by this module is not appropriate (i.e. not calculating
    tags for a CPython interpreter).

    The specific tags generated are:

    - ``<interpreter>-<abi>-<platform>``

    The ``"none"`` ABI will be added if it was not explicitly provided.

    :param str interpreter: The name of the interpreter. Defaults to being
                            calculated.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    pass


def _py_interpreter_range(py_version: PythonVersion) -> Iterator[str]:
    """
    Yields Python versions in descending order.

    After the latest version, the major-only version will be yielded, and then
    all previous versions of that major version.
    """
    pass


def compatible_tags(
    python_version: PythonVersion | None = None,
    interpreter: str | None = None,
    platforms: Iterable[str] | None = None,
) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter compatible with the Python version
    specified by ``python_version``.

    The specific tags generated are:

    - ``py*-none-<platform>``
    - ``<interpreter>-none-any`` if ``interpreter`` is provided
    - ``py*-none-any``

    :param Sequence python_version: A one- or two-item sequence representing the
                                 compatible version of Python. Defaults to
                                 ``sys.version_info[:2]``.
    :param str interpreter: The name of the interpreter (if known), e.g.
                            ``"cp38"``. Defaults to the current interpreter.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    """
    pass


def _mac_arch(arch: str, is_32bit: bool = _32_BIT_INTERPRETER) -> str:
    pass


def _mac_binary_formats(version: AppleVersion, cpu_arch: str) -> list[str]:
    pass


def mac_platforms(
    version: AppleVersion | None = None, arch: str | None = None
) -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for macOS.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.

    :param tuple version: A two-item tuple representing the version of macOS.
                          Defaults to the current system's version.
    :param str arch: The CPU architecture. Defaults to the architecture of the
                     current system, e.g. ``"x86_64"``.

    .. note::
        Equivalent support for the other major platforms is purposefully not
        provided:

        - On Windows, platform compatibility is statically specified
        - On Linux, code must be run on the system itself to determine
          compatibility
    """
    pass


def ios_platforms(
    version: AppleVersion | None = None, multiarch: str | None = None
) -> Iterator[str]:
    """

    Yields the :attr:`~Tag.platform` tags for iOS.

    :param tuple version: A two-item tuple representing the version of iOS.
                          Defaults to the current system's version.
    :param str multiarch: The CPU architecture+ABI to be used. This should be in
                          the format by ``sys.implementation._multiarch`` (e.g.,
                          ``arm64_iphoneos`` or ``x86_64_iphonesimulator``).
                          Defaults to the current system's multiarch value.

    .. note::
        Behavior of this method is undefined if invoked on non-iOS platforms
        without providing explicit version and multiarch arguments.
    """
    pass


def android_platforms(
    api_level: int | None = None, abi: str | None = None
) -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for Android. If this function is invoked on
    non-Android platforms, the ``api_level`` and ``abi`` arguments are required.

    :param int api_level: The maximum `API level
        <https://developer.android.com/tools/releases/platforms>`__ to return. Defaults
        to the current system's version, as returned by ``platform.android_ver``.
    :param str abi: The `Android ABI <https://developer.android.com/ndk/guides/abis>`__,
        e.g. ``arm64_v8a``. Defaults to the current system's ABI , as returned by
        ``sysconfig.get_platform``. Hyphens and periods will be replaced with
        underscores.
    """
    pass


def _linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER) -> Iterator[str]:
    pass


def _emscripten_platforms() -> Iterator[str]:
    pass


def _generic_platforms() -> Iterator[str]:
    pass


def platform_tags() -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for the running interpreter.
    """
    pass


def interpreter_name() -> str:
    """
    Returns the name of the running interpreter.

    Some implementations have a reserved, two-letter abbreviation which will
    be returned when appropriate.

    This typically acts as the prefix to the :attr:`~Tag.interpreter` tag.
    """
    pass


def interpreter_version(*, warn: bool = False) -> str:
    """
    Returns the running interpreter's version.

    This typically acts as the suffix to the :attr:`~Tag.interpreter` tag.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    pass


def _version_nodot(version: PythonVersion) -> str:
    pass


def sys_tags(*, warn: bool = False) -> Iterator[Tag]:
    """
    Yields the sequence of tag triples that the running interpreter supports.

    The iterable is ordered so that the best-matching tag is first in the
    sequence. The exact preferential order to tags is interpreter-specific, but
    in general the tag importance is in the order of:

    1. Interpreter
    2. Platform
    3. ABI

    This order is due to the fact that an ABI is inherently tied to the
    platform, but platform-specific code is not necessarily tied to the ABI. The
    interpreter is the most important tag as it dictates basic support for any
    wheel.

    The function returns an iterable in order to allow for the possible
    short-circuiting of tag generation if the entire sequence is not necessary
    and tag calculation happens to be expensive.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.

    .. versionchanged:: 21.3
        Added the `pp3-none-any` tag (:issue:`311`).
    .. versionchanged:: 27.0
        Added the `abi3t` tag (:issue:`1099`).
    """
    pass


def create_compatible_tags_selector(
    tags: Iterable[Tag],
) -> Callable[[Iterable[tuple[_T, AbstractSet[Tag]]]], Iterator[_T]]:
    """Create a callable to select things compatible with supported tags.

    This function accepts an ordered sequence of tags, with the preferred
    tags first.

    The returned callable accepts an iterable of tuples (thing, set[Tag]),
    and returns an iterator of things, with the things with the best
    matching tags first.

    Example to select compatible wheel filenames:

    >>> from packaging import tags
    >>> from packaging.utils import parse_wheel_filename
    >>> selector = tags.create_compatible_tags_selector(tags.sys_tags())
    >>> filenames = ["foo-1.0-py3-none-any.whl", "foo-1.0-py2-none-any.whl"]
    >>> list(selector([
    ...     (filename, parse_wheel_filename(filename)[-1]) for filename in filenames
    ... ]))
    ['foo-1.0-py3-none-any.whl']

    .. versionadded:: 26.1
    """
    pass
