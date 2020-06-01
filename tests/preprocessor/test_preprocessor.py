from hypothesis import given, example
from hypothesis.strategies import text, characters
import csv
import pytest

from company_graph.normalizer import *

@pytest.fixture(scope='module')
def stopwords():
    with open('../company_names_stopwords.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        test_pairs_stopwords = [tuple(line) for line in reader]
    return test_pairs_stopwords


@given(text() | characters())
def test_strip_punc(s):
    stripped_s = STRIP_PUNCTUATION(s)
    assert len([p for p in string.punctuation if p in stripped_s]) == 0

@given(text() | characters())
@example("ABC  ABC ABC")
@example("A B  A  B  ")
def test_multi_ws(s):

    # Are these still present?
    copy_s = s

    assert STRIP_MULTIPLE_WHITESPACE(copy_s).find("  ") == -1

    # Did we remove desired whitespace?
    original_tokens = [token for token in s.split() if token != " "]
    stripped_tokens = STRIP_MULTIPLE_WHITESPACE(copy_s).split()
    assert original_tokens == stripped_tokens

def test_stopwords(stopwords):
    for raw, expected in stopwords:
        assert STRIP_STOPWORDS(raw) == expected

    s = ['ABC-ABC', 'ABC.ABC', '.ABC.ABC', 'ABC at ABC', 'ABC ABC', 'ABC  ABC  ']
    p = Preprocessor()
    for example in s:
        assert "abc abc" == p(example)


