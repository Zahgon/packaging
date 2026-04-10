from __future__ import annotations

from pathlib import Path

from packaging.requirements import Requirement

from . import add_attributes

DIR = Path(__file__).parent.resolve()


class TimeRequirementSuite:
    rounds = 4

    def setup(self) -> None:
        pass

    @add_attributes(pretty_name="Requirement constructor")
    def time_constructor(self) -> None:
        pass
