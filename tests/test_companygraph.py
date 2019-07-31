from company_graph.cg import CompanyGraph
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
        assert self.cg(2844978) == 'cisco'
        assert self.cg.id2id(2844978) == 1063


if __name__ == "__main__":
    unittest.main()
