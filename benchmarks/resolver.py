from __future__ import annotations

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from . import add_attributes


class TimeResolverSuite:
    rounds = 4

    def setup(self) -> None:
        pass

    @add_attributes(pretty_name="Resolver-style loop")
    def time_resolver_loop(self) -> None:
        pass
