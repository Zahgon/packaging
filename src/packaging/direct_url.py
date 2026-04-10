from __future__ import annotations

import dataclasses
import re
import urllib.parse
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from collections.abc import Collection

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

__all__ = [
    "ArchiveInfo",
    "DirInfo",
    "DirectUrl",
    "DirectUrlValidationError",
    "VcsInfo",
]


def __dir__() -> list[str]:
    return __all__


_T = TypeVar("_T")


class _FromMappingProtocol(Protocol):  # pragma: no cover
    @classmethod
    def _from_dict(cls, d: Mapping[str, Any]) -> Self: ...


_FromMappingProtocolT = TypeVar("_FromMappingProtocolT", bound=_FromMappingProtocol)


def _json_dict_factory(data: list[tuple[str, Any]]) -> dict[str, Any]:
    pass


def _get(d: Mapping[str, Any], expected_type: type[_T], key: str) -> _T | None:
    """Get a value from the dictionary and verify it's the expected type."""
    pass


def _get_required(d: Mapping[str, Any], expected_type: type[_T], key: str) -> _T:
    """Get a required value from the dictionary and verify it's the expected type."""
    pass


def _get_object(
    d: Mapping[str, Any], target_type: type[_FromMappingProtocolT], key: str
) -> _FromMappingProtocolT | None:
    """Get a dictionary value from the dictionary and convert it to a dataclass."""
    pass


_PEP610_USER_PASS_ENV_VARS_REGEX = re.compile(
    r"^\$\{[A-Za-z0-9-_]+\}(:\$\{[A-Za-z0-9-_]+\})?$"
)


def _strip_auth_from_netloc(netloc: str, safe_user_passwords: Collection[str]) -> str:
    pass


def _strip_url(url: str, safe_user_passwords: Collection[str]) -> str:
    """url with user:password part removed unless it is formed with
    environment variables as specified in PEP 610, or it is a safe user:password
    such as `git`.
    """
    pass


class DirectUrlValidationError(Exception):
    """Raised when when input data is not spec-compliant."""

    context: str | None = None
    message: str

    def __init__(
        self,
        cause: str | Exception,
        *,
        context: str | None = None,
    ) -> None:
        if isinstance(cause, DirectUrlValidationError):
            if cause.context:
                self.context = (
                    f"{context}.{cause.context}" if context else cause.context
                )
            else:
                self.context = context  # pragma: no cover
            self.message = cause.message
        else:
            self.context = context
            self.message = str(cause)

    def __str__(self) -> str:
        if self.context:
            return f"{self.message} in {self.context!r}"
        return self.message


class _DirectUrlRequiredKeyError(DirectUrlValidationError):
    def __init__(self, key: str) -> None:
        super().__init__("Missing required value", context=key)


@dataclasses.dataclass(frozen=True, init=False)
class VcsInfo:
    vcs: str
    commit_id: str
    requested_revision: str | None = None

    def __init__(
        self,
        *,
        vcs: str,
        commit_id: str,
        requested_revision: str | None = None,
    ) -> None:
        object.__setattr__(self, "vcs", vcs)
        object.__setattr__(self, "commit_id", commit_id)
        object.__setattr__(self, "requested_revision", requested_revision)

    @classmethod
    def _from_dict(cls, d: Mapping[str, Any]) -> Self:
        # We can't validate vcs value because is not closed.
        pass


@dataclasses.dataclass(frozen=True, init=False)
class ArchiveInfo:
    hashes: Mapping[str, str] | None = None

    def __init__(
        self,
        *,
        hashes: Mapping[str, str] | None = None,
    ) -> None:
        object.__setattr__(self, "hashes", hashes)

    @classmethod
    def _from_dict(cls, d: Mapping[str, Any]) -> Self:
        pass


@dataclasses.dataclass(frozen=True, init=False)
class DirInfo:
    editable: bool | None = None

    def __init__(
        self,
        *,
        editable: bool | None = None,
    ) -> None:
        object.__setattr__(self, "editable", editable)

    @classmethod
    def _from_dict(cls, d: Mapping[str, Any]) -> Self:
        pass


@dataclasses.dataclass(frozen=True, init=False)
class DirectUrl:
    """A class representing a direct URL."""

    url: str
    archive_info: ArchiveInfo | None = None
    vcs_info: VcsInfo | None = None
    dir_info: DirInfo | None = None
    subdirectory: str | None = None  # XXX Path or str?

    def __init__(
        self,
        *,
        url: str,
        archive_info: ArchiveInfo | None = None,
        vcs_info: VcsInfo | None = None,
        dir_info: DirInfo | None = None,
        subdirectory: str | None = None,
    ) -> None:
        object.__setattr__(self, "url", url)
        object.__setattr__(self, "archive_info", archive_info)
        object.__setattr__(self, "vcs_info", vcs_info)
        object.__setattr__(self, "dir_info", dir_info)
        object.__setattr__(self, "subdirectory", subdirectory)

    @classmethod
    def _from_dict(cls, d: Mapping[str, Any]) -> Self:
        pass

    @classmethod
    def from_dict(cls, d: Mapping[str, Any], /) -> Self:
        """Create and validate a DirectUrl instance from a JSON dictionary."""
        pass

    def to_dict(
        self,
        *,
        generate_legacy_hash: bool = False,
        strip_user_password: bool = True,
        safe_user_passwords: Collection[str] = ("git",),
    ) -> Mapping[str, Any]:
        """Convert the DirectUrl instance to a JSON dictionary.

        :param generate_legacy_hash: If True, include a legacy `hash` field in
            `archive_info` for backward compatibility with tools that don't
            support the `hashes` field.
        :param strip_user_password: If True, strip user:password from the URL
            unless it is formed with environment variables as specified in PEP
            610, or it is a safe user:password such as `git`.
        :param safe_user_passwords: A collection of user:password strings that
            should not be stripped from the URL even if `strip_user_password` is
            True.
        """
        pass

    def validate(self) -> None:
        """Validate the DirectUrl instance against the specification.

        Raises :class:`DirectUrlValidationError` if invalid.
        """
        pass
