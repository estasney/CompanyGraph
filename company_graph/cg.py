import pickle
from typing import Union, Optional

import pkg_resources

from company_graph.normalizer import Preprocessor
from company_graph.rules import RuleMatcher


class CompanyGraph(object):

    def __init__(self, preprocessor=Preprocessor, rules=RuleMatcher):
        self.graph = self.load_graph()
        self.preprocessor = preprocessor(rules=rules)

    def load_graph(self):

        data_path = pkg_resources.resource_filename('company_graph', 'data/graph.pkl')
        with open(data_path, "rb") as pfile:
            return pickle.load(pfile)

    def __contains__(self, item):
        if self.preprocessor:
            if isinstance(item, str):
                item = self.preprocessor(item)
        if self.graph.has_node(item):
            return True
        else:
            return item in self.preprocessor.rules

    def __call__(self, item: Optional[Union[int, str]]):
        if not item:
            return None

        if isinstance(item, int):
            return self.id2string(item)

        else:
            return self.string2id(item)

    def string2id(self, item: str) -> Optional[id]:

        # String lookups will have one id mapping made available
        item_result = self.preprocessor(item)
        if not item_result:
            return None

        try:
            route = list(self.graph[item_result])[0]
        except (KeyError, IndexError) as e:
            return None

        return route

    def id2id(self, item: int) -> int:

        # Does the id have any redirects?

        # If not, return id
        has_node = self.graph.has_node(item)
        if not has_node:
            return item
        routes = self.graph[item]
        if not routes:
            return item

        # If so...
        # Is the gravity of this node greater than all redirects?

        current_gravity = self.graph.nodes[item].get('g', 0)
        competing_node = max(routes.items(), key=lambda x: x[1].get('g', 0))

        # Yes? Stop here
        if current_gravity >= competing_node[1].get('g', 0):
            return item

        # No? Follow greater gravity
        return self.id2id(competing_node[0])

    def id2string(self, item) -> Optional[str]:

        # Does the id have any redirects?
        item_result = self.id2id(item)

        # Generate potential names via predecessors
        # Filter out redirects, these have a gravity attribute

        predecessors = self.graph.pred.get(item_result)
        if not predecessors:
            return None

        potential_names = [(name, data) for name, data in predecessors.items() if data and 'n' in data]
        if not potential_names:
            return None

        else:
            return max(potential_names, key=lambda x: x[1]['n'])[0]
