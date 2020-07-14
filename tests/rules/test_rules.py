import pytest

@pytest.fixture(scope='module')
def cg():
    from company_graph.cg import CompanyGraph
    cg = CompanyGraph()
    return cg

@pytest.mark.parametrize("given,expected,equals", [("PrefixIBM", "ibm", False),
                                                   ("Prefix IBM", "ibm", True),
                                                   ("Prefix Oracle", "oracle", True),
                                                   ("Oracle Systems, Inc", "oracle", True),
                                                   ("Prefix Accenture", "accenture", False),
                                                   ("Accenture Suffix", "accenture", True),
                                                   ("Hewlett Packard", "hewlett packard", True),
                                                   ("HPE", "hewlett packard", True),
                                                   ("AT&T", "att", True),
                                                   ("ATT", "att", True)])
def test_rules(given, expected, equals, cg):
    company_id = cg(given)
    company_str = cg(company_id)
    if equals:
        assert company_str == expected
    else:
        assert company_str != expected