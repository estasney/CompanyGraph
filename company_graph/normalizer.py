import re
import string
from functools import partial
from typing import Optional, List, Callable, TypeVar, Union, Type

from company_graph.rules import RuleMatcher



def strip_match(s, pattern):
    return pattern.sub(" ", s)


def to_lowercase(s):
    return s.lower()


RE_PUNCTUATION = re.compile(r'([%s])+' % re.escape(string.punctuation))
RE_MULTIPLE_WHITESPACE = re.compile(r"( {2,})")
STOPWORDS = ['for', 'global', 'by', 'international', 'technologies', 'the', 'group', 'systems', 'of', 'corporation',
             'and', 'limited', 'llc', 'ltd', 'inc', 'company', 'consulting', 'at']
RE_STOPWORDS = re.compile("({})(?![A-z] ?)".format("|".join(STOPWORDS)), re.IGNORECASE)

STRIP_PUNCTUATION = partial(strip_match, pattern=RE_PUNCTUATION)
STRIP_MULTIPLE_WHITESPACE = partial(strip_match, pattern=RE_MULTIPLE_WHITESPACE)
STRIP_STOPWORDS = partial(strip_match, pattern=RE_STOPWORDS)
TO_LOWERCASE = to_lowercase
STRIP_STRING = lambda x: x.strip()


class Preprocessor(object):
    DEFAULT_STRING_PROCESSORS = [STRIP_STOPWORDS, STRIP_PUNCTUATION, STRIP_MULTIPLE_WHITESPACE, TO_LOWERCASE,
                                 STRIP_STRING]

    def __init__(self, rules: Optional[RuleMatcher] = RuleMatcher, processors: Optional[List[Callable]] = None):
        if processors is None:
            processors = Preprocessor.DEFAULT_STRING_PROCESSORS
        self.processors = processors
        self.rules = rules

    def __call__(self, s: Optional[str]) -> Optional[str]:
        if not s:
            return s

        s_post_rule, was_matched = self.rules.run(s)
        if was_matched:
            return s_post_rule

        s_copy = s
        if self.processors:
            for sp in self.processors:
                if not s_copy:  # In case we've removed everything
                    return s
                s_copy = sp(s_copy)

        s_copy = s_copy.strip()
        if not s_copy:
            return s
        return s_copy
