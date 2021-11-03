import csv
import logging
import pickle
from typing import List, NamedTuple

import click

from company_graph.cg import CompanyGraph

logger = logging.getLogger(__name__)


class NameEdge(NamedTuple):
    source: str
    target: int
    n: int


def read_rows(fp, cg: CompanyGraph) -> List[NameEdge]:
    rows = []
    with open(fp, "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip headers
        for company_id, company_name, count in reader:
            company_id, count = int(company_id), int(count)
            company_name_norm = cg.preprocessor(company_name)
            if not company_name_norm:
                logger.info(f"Skipping {company_name} - it appears in stoplist")
                continue
            else:
                rows.append(NameEdge(source=company_name, target=company_id, n=count))
    return rows


@click.command()
@click.argument("input-file", type=click.Path(exists=True))
@click.argument("output-file", type=click.Path())
@click.option("--min-count", default=10)
def append_data(input_file, output_file, min_count):
    cg = CompanyGraph()
    new_rows = read_rows(input_file, cg)

    g = cg.graph
    for row in new_rows:
        if g.has_edge(row.source, row.target):
            g[row.source][row.target]["n"] += row.n
        else:
            if row.n >= min_count:
                g.add_edge(row.source, row.target, n=row.n)

    # Names should have 1 possible id candidate

    name_nodes = (node for node in g.nodes if isinstance(node, str))
    for name in name_nodes:
        name_edges = list(g[name].items())
        if len(name_edges) == 1:
            continue
        max_edge = max(name_edges, key=lambda x: x[1]["n"])
        others = [e for e in name_edges if e != max_edge]
        for o in others:
            logger.info(f"Removing Edge {name}-{o[0]}")
            g.remove_edge(name, o[0])
            logger.info(f"Adding Edge {o[0]}-{max_edge[0]}")
            g.add_edge(o[0], max_edge[0], g=o[1]["n"])

    def gravity(company_id):
        preds = g.pred.get(company_id)
        if not preds:
            return 0
        preds = list(preds.items())
        return sum([x[1]["n"] if "n" in x[1] else x[1]["g"] for x in preds])

    id_nodes = (node for node in g.nodes if isinstance(node, int))
    for i in id_nodes:
        g.nodes[i]["g"] = gravity(i)

    with open(output_file, "wb") as fp:
        pickle.dump(g, fp)

    cg.graph = g
    print(cg(2844978))


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    append_data()
