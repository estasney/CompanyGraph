import re
import typing
from abc import ABC
from functools import partial

ends_with = partial(lambda x, y: x.endswith(y))
starts_with = partial(lambda x, y: x.startswith(y))
sub_with = partial(lambda x, y, z: x.replace(y, z))
re_match = partial(lambda x, y: y.search(x) is not None)


class Action(ABC):

    def run(self, x):
        raise NotImplementedError


class Match(ABC):
    def __init__(self, matched_type=str):
        self.matched_type = matched_type

    def _type_check(self, x):
        return isinstance(x, self.matched_type)

    def run(self, x):
        raise NotImplementedError


class EndsWith(Match):

    def __init__(self, char_pattern: str, matched_type=str):
        super().__init__(matched_type)
        self.matched_type = matched_type
        self.char = char_pattern

    def run(self, x):
        if not self._type_check(x):
            return False
        return x.endswith(self.char)


class StartsWith(Match):

    def __init__(self, char_pattern: str, matched_type=str):
        super().__init__(matched_type)
        self.matched_type = matched_type
        self.char = char_pattern

    def run(self, x):
        if not self._type_check(x):
            return False
        return x.startswith(self.char)


class MatchesRegex(Match):

    def __init__(self, pattern: typing.Union[str, typing.Pattern], matched_type=str):
        super().__init__(matched_type)
        self.matched_type = matched_type
        self.char = pattern
        if isinstance(self.char, str):
            self.f = partial(re.search, pattern=self.char)
        else:
            self.f = self.char.search

    def run(self, x: str):
        if not self._type_check(x):
            return False
        return self.f(string=x) is not None


class Sub(Action):

    def __init__(self, old: typing.Union[str, typing.Pattern], new: str):
        self.old = old
        self.new = new
        if isinstance(self.old, str):
            self.f = partial(lambda x: x.replace(self.old, self.new))
        else:
            self.f = partial(lambda ptrn, repl, x: ptrn.sub(repl, x), ptrn=self.old, repl=self.new)

    def run(self, x: str):
        x = self.f(x=x)
        return x


class Drop(Action):

    def run(self, x):
        return None


class Return(Action):

    def __init__(self, return_value):
        self.return_value = return_value

    def run(self, x):
        return self.return_value


class Pattern(object):
    def __init__(self, match: Match, action: Action):
        self.match = match
        self.action = action

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, x: str, *args, **kwargs):
        if self.match.run(x):
            x = self.action.run(x)
            return x, True
        return x, False


"""
Composed Patterns
"""


def __regex_factory(template, *flags, **kwargs):
    return re.compile(template.format(**kwargs), *flags)


def __regex_factory_i_escape(template, pattern):
    return __regex_factory(template, re.IGNORECASE, pattern=re.escape(pattern))


__startswith_template = r"^({pattern})"
__endswith_template = r"({pattern})$"
__contains_token_template = r"\b({pattern})\b"

_contains_ibm = __regex_factory_i_escape(__contains_token_template, "ibm")
contains_ibm = Pattern(
        match=MatchesRegex(pattern=_contains_ibm),
        action=Return(return_value="ibm")
        )

_startswith_oracle = __regex_factory_i_escape(__contains_token_template, "oracle")
starts_with_oracle = Pattern(
        match=MatchesRegex(pattern=_startswith_oracle),
        action=Return(return_value="oracle")
        )

PATTERNS = [
    starts_with_oracle, contains_ibm
    ]
