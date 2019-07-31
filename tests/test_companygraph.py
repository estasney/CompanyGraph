import pickle

from hypothesis import given, example
from hypothesis.strategies import text, characters
import pkg_resources
import csv

from company_graph import CompanyGraph
from company_graph.normalizer import *

import unittest


class TestCompanyGraph(unittest.TestCase):

    def setUp(self) -> None:
        self.cg = CompanyGraph

    def test_graph_loads(self):
        try:
            self.cg()
        except:
            raise AssertionError

    def test_company2id(self):
        self.cg = self.cg()
        assert self.cg('Cisco') == 1063
        assert self.cg('Cisco Talos') == 1063
        assert self.cg('Google') == 1441
        assert self.cg(2844978) == 1063








if __name__ == "__main__":
    unittest.main()
