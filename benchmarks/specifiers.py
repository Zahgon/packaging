from __future__ import annotations

from pathlib import Path

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from . import add_attributes

DIR = Path(__file__).parent.resolve()


class TimeSpecSuite:
    rounds = 4

    SIMPLE_SPEC = ">0.5"
    COMPLEX_SPEC = ">=3.8,!=3.9.*,!=3.10.0,!=3.10.1,~=3.10.2,<3.14,!=3.11.0,!=3.12.0"
    COMPATIBLE_SPEC = "~=3.10"

    def setup(self) -> None:
        pass

    def _make_cold(self, spec: SpecifierSet) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet constructor")
    def time_constructor(self) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet contains (cold)")
    def time_contains_cold(self) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet contains (warm)")
    def time_contains_warm(self) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet contains (complex, warm)")
    def time_contains_complex_warm(self) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet filter (simple, cold)")
    def time_filter_simple_cold(self) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet filter (simple, warm)")
    def time_filter_simple_warm(self) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet filter (complex, cold)")
    def time_filter_complex_cold(self) -> None:
        pass

    @add_attributes(pretty_name="SpecifierSet filter (complex, warm)")
    def time_filter_complex_warm(self) -> None:
        pass

    # Only warm filter for compatible (~=): cold and contains paths are already
    # well covered by the simple/complex specifier benchmarks above.
    @add_attributes(pretty_name="SpecifierSet filter (compatible, warm)")
    def time_filter_compatible_warm(self) -> None:
        pass
