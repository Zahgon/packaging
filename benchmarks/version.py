from __future__ import annotations

from pathlib import Path

from packaging.version import InvalidVersion, Version

from . import add_attributes

DIR = Path(__file__).parent.resolve()


def valid_version(v: str) -> Version | None:
    pass


class TimeVersionSuite:
    rounds = 4

    def setup(self) -> None:
        pass

    @add_attributes(pretty_name="Version constructor")
    def time_constructor(self) -> None:
        pass

    @add_attributes(pretty_name="Version hash")
    def time_hash(self) -> None:
        pass

    @add_attributes(pretty_name="Version hash (warm cache)")
    def time_hash_warm(self) -> None:
        pass

    @add_attributes(pretty_name="Version __str__")
    def time_str(self) -> None:
        pass

    @add_attributes(pretty_name="Version sorting (cold cache)")
    def time_sort_cold(self) -> None:
        """Sorting when _key needs to be calculated during comparison."""
        pass

    @add_attributes(pretty_name="Version sorting (warm cache)")
    def time_sort_warm(self) -> None:
        """Sorting when _key is already cached."""
        pass
