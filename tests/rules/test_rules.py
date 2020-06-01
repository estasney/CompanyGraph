import pytest

@pytest.fixture(scope='module')
def cg():
    from company_graph.cg import CompanyGraph
    cg = CompanyGraph()
    return cg