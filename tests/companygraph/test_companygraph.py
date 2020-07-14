import pytest

@pytest.fixture(scope='module')
def cg():
    from company_graph.cg import CompanyGraph
    cg = CompanyGraph()
    return cg

@pytest.mark.parametrize("given,expected", [("Cisco", 1063),
                                            ("Cisco Talos", 1063),
                                            ("Google", 1441),
                                            (2844978, "cisco"),
                                            ])
def test_company2id_call(given, expected, cg):
    assert cg(given) == expected



