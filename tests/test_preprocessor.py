from hypothesis import given
from hypothesis.strategies import text, characters
import csv

from company_graph.normalizer import *

import unittest


class TestRegex(unittest.TestCase):

    def setUp(self) -> None:
        with open('company_names_stopwords.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.test_pairs_stopwords = [tuple(line) for line in reader]

    @given(text() | characters())
    def test_strip_punc(self, s):
        stripped_s = STRIP_PUNCTUATION(s)
        assert len([p for p in string.punctuation if p in stripped_s]) == 0

    @given(text() | characters())
    def test_multi_ws(self, s):
        # Are these still present?
        copy_s = s

        assert STRIP_MULTIPLE_WHITESPACE(copy_s).find("  ") == -1

        # Did we remove desired whitespace?
        original_tokens = [token for token in s.split(" ") if token != " "]
        stripped_tokens = STRIP_MULTIPLE_WHITESPACE(copy_s).split(" ")
        assert original_tokens == stripped_tokens

    def test_stopwords(self):
        for raw, expected in self.test_pairs_stopwords:
            if STRIP_STOPWORDS(raw) != expected:
                raise AssertionError("{} should have been {} but was {}".format(raw, expected, STRIP_STOPWORDS(raw)))


if __name__ == "__main__":
    unittest.main()
