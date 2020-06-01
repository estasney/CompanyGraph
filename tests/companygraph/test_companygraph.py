import pytest

@pytest.fixture(scope='module')
def cg():
    from company_graph.cg import CompanyGraph
    cg = CompanyGraph()
    return cg

def test_company2id(cg):
    assert cg('Cisco') == 1063
    assert cg('Cisco Talos') == 1063
    assert cg('Google') == 1441
    assert cg(2844978) == 'cisco'
    assert cg.id2id(2844978) == 1063

