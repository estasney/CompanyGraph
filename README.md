### CompanyGraph

#### Install
`pip install company-graph`

#### Build
```python setup.py sdist bdist_wheel```

```twine upload dist/*```

#### Usage
```python
from company_graph import CompanyGraph

cg = CompanyGraph()

# Generalize company ids
>>> cg.id2id(1697742)
1063

# Deterministic company id from string
>>> cg('Cisco')
1063
>>> cg('Talos Group at Cisco')
1063

# Deterministic company name from id
>>> cg(1063)
'cisco'
```