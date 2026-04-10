from __future__ import annotations

from pathlib import Path

from packaging.markers import Marker

from . import add_attributes

DIR = Path(__file__).parent.resolve()


class TimeMarkerSuite:
    rounds = 4

    def setup(self) -> None:
        pass

    @add_attributes(pretty_name="Marker constructor")
    def time_constructor(self) -> None:
        pass

    @add_attributes(pretty_name="Marker evaluate")
    def time_evaluate(self) -> None:
        pass
