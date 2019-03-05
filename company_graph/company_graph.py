import pickle
import re
import string

import pkg_resources


class Preprocessor(object):
    punct_re = re.compile(r'([%s])+' % re.escape(string.punctuation))
    multi_ws = re.compile(r"( {2,})")

    def __init__(self):
        pass

    def __call__(self, s):
        s = s.lower()
        s = self.punct_re.sub(string=s, repl="")
        s = self.multi_ws.sub(string=s, repl=" ")
        s = s.strip()
        return s


class CompanyGraph(object):

    def __init__(self, preprocessor=Preprocessor):
        self.graph = self.load_graph()
        self.preprocessor = preprocessor()

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
            return False

    def __call__(self, item):
        if self.preprocessor:
            if isinstance(item, str):
                item = self.preprocessor(item)
        if not self.graph.has_node(item):
            return None

        if isinstance(item, str):
            return self.string2id(item)

        else:
            return self.id2string(item)

        # Is it a company_id? If so follow redirects

    def string2id(self, item):

        # String lookups will have one id mapping made available

        route = list(self.graph[item])[0]
        return route

    def id2id(self, item):

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

    def id2string(self, item):

        # Does the id have any redirects?
        item = self.id2id(item)

        # Generate potential names via predecessors
        # Filter out redirects, these have a gravity attribute
        potential_names = list(filter(lambda x: x[1].get('n') is not None, self.graph.pred.get(item).items()))

        if not potential_names:
            return None

        else:
            return max(potential_names, key=lambda x: x[1]['n'])[0]
