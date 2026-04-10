from __future__ import annotations

import contextlib
import re
from dataclasses import dataclass
from typing import Generator, Mapping, NoReturn

from .specifiers import Specifier


@dataclass
class Token:
    name: str
    text: str
    position: int


class ParserSyntaxError(Exception):
    """The provided source text could not be parsed correctly."""

    def __init__(
        self,
        message: str,
        *,
        source: str,
        span: tuple[int, int],
    ) -> None:
        self.span = span
        self.message = message
        self.source = source

        super().__init__()

    def __str__(self) -> str:
        marker = " " * self.span[0] + "~" * (self.span[1] - self.span[0]) + "^"
        return f"{self.message}\n    {self.source}\n    {marker}"


DEFAULT_RULES: dict[str, re.Pattern[str]] = {
    "LEFT_PARENTHESIS": re.compile(r"\("),
    "RIGHT_PARENTHESIS": re.compile(r"\)"),
    "LEFT_BRACKET": re.compile(r"\["),
    "RIGHT_BRACKET": re.compile(r"\]"),
    "SEMICOLON": re.compile(r";"),
    "COMMA": re.compile(r","),
    "QUOTED_STRING": re.compile(
        r"""
            (
                ('[^']*')
                |
                ("[^"]*")
            )
        """,
        re.VERBOSE,
    ),
    "OP": re.compile(r"(===|==|~=|!=|<=|>=|<|>)"),
    "BOOLOP": re.compile(r"\b(or|and)\b"),
    "IN": re.compile(r"\bin\b"),
    "NOT": re.compile(r"\bnot\b"),
    "VARIABLE": re.compile(
        r"""
            \b(
                python_version
                |python_full_version
                |os[._]name
                |sys[._]platform
                |platform_(release|system)
                |platform[._](version|machine|python_implementation)
                |python_implementation
                |implementation_(name|version)
                |extras?
                |dependency_groups
            )\b
        """,
        re.VERBOSE,
    ),
    "SPECIFIER": re.compile(
        Specifier._specifier_regex_str,
        re.VERBOSE | re.IGNORECASE,
    ),
    "AT": re.compile(r"\@"),
    "URL": re.compile(r"[^ \t]+"),
    "IDENTIFIER": re.compile(r"\b[a-zA-Z0-9][a-zA-Z0-9._-]*\b"),
    "VERSION_PREFIX_TRAIL": re.compile(r"\.\*"),
    "VERSION_LOCAL_LABEL_TRAIL": re.compile(r"\+[a-z0-9]+(?:[-_\.][a-z0-9]+)*"),
    "WS": re.compile(r"[ \t]+"),
    "END": re.compile(r"$"),
}


class Tokenizer:
    """Context-sensitive token parsing.

    Provides methods to examine the input stream to check whether the next token
    matches.
    """

    def __init__(
        self,
        source: str,
        *,
        rules: Mapping[str, re.Pattern[str]],
    ) -> None:
        self.source = source
        self.rules = rules
        self.next_token: Token | None = None
        self.position = 0

    def consume(self, name: str) -> None:
        """Move beyond provided token name, if at current position."""
        pass

    def check(self, name: str, *, peek: bool = False) -> bool:
        """Check whether the next token has the provided name.

        By default, if the check succeeds, the token *must* be read before
        another check. If `peek` is set to `True`, the token is not loaded and
        would need to be checked again.
        """
        pass

    def expect(self, name: str, *, expected: str) -> Token:
        """Expect a certain token name next, failing with a syntax error otherwise.

        The token is *not* read.
        """
        pass

    def read(self) -> Token:
        """Consume the next token and return it."""
        pass

    def raise_syntax_error(
        self,
        message: str,
        *,
        span_start: int | None = None,
        span_end: int | None = None,
    ) -> NoReturn:
        """Raise ParserSyntaxError at the given position."""
        pass

    @contextlib.contextmanager
    def enclosing_tokens(
        self, open_token: str, close_token: str, *, around: str
    ) -> Generator[None, None, None]:
        pass
