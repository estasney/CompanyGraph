import re
import string
import typing
from functools import partial


def strip_match(s, pattern):
    return pattern.sub("", s)


def to_lowercase(s):
    return s.lower()


RE_PUNCTUATION = re.compile(r'([%s])+' % re.escape(string.punctuation))
RE_MULTIPLE_WHITESPACE = re.compile(r"( {2,})")
STOPWORDS = ['for', 'global', 'by', 'international', 'technologies', 'the', 'group', 'systems', 'of', 'corporation',
             'and', 'limited', 'llc', 'ltd', 'inc', 'company', 'consulting']
RE_STOPWORDS = re.compile("({})(?![A-z] ?)".format("|".join(STOPWORDS)), re.IGNORECASE)

STRIP_PUNCTUATION = partial(strip_match, pattern=RE_PUNCTUATION)
STRIP_MULTIPLE_WHITESPACE = partial(strip_match, pattern=RE_MULTIPLE_WHITESPACE)
STRIP_STOPWORDS = partial(strip_match, pattern=RE_STOPWORDS)
TO_LOWERCASE = to_lowercase


class Preprocessor(object):
    DEFAULT_STRING_PROCESSORS = [STRIP_STOPWORDS, STRIP_PUNCTUATION, STRIP_MULTIPLE_WHITESPACE, TO_LOWERCASE]

    def __init__(self, *args: typing.Callable):
        self.string_processors = self.DEFAULT_STRING_PROCESSORS if not args else args

    def __call__(self, s):
        ps = s  # Keep original reference
        for sp in self.string_processors:
            if not ps:  # In case we've removed everything
                return s
            ps = sp(ps)
        ps = ps.strip()
        if not ps:
            return s
        return ps
