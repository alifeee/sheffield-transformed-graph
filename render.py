"""Render the graph.yaml into a webpage"""

from datetime import datetime
from textwrap import dedent, wrap
import random
import yaml
from pybars import Compiler
import igraph as ig

INPUT_FILE = "graph.yaml"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    graph = yaml.safe_load(file)

# make edges into objects
graph["edges"] = [edge.split(", ") for edge in graph["edges"]]

# error if any edges do not exist
for edge in graph["edges"]:
    if edge[0] not in graph["nodes"] or edge[1] not in graph["nodes"]:
        raise ValueError(f"{edge[0]} or {edge[1]} are not nodes")

# █▀▀ █▀▄▀█ █
# █▄█ █ ▀ █ █▄▄

with open("graph.gml", "w", encoding="utf-8") as file:
    file.write(
        f'Creator "alifeee on {datetime.now().strftime("%a %b %d %H:%M:%S %Y")}"\n'
    )
    file.write("graph [\n")
    node_ids = {}
    for node_id, node_label in graph["nodes"].items():
        node_ids[node_id] = len(node_ids)
        file.write(
            dedent(
                f"""\
            node [
              id {node_ids[node_id]}
              label "{node_label}"
            ]
        """
            )
        )
    for [e_from, e_to] in graph["edges"]:
        file.write(
            dedent(
                f"""\
            edge
            [
              source {node_ids[e_from]}
              target {node_ids[e_to]}
            ]
            """
            )
        )
    file.write("]")

# █ █ █▄▄ █▀
# █▀█ █▄█ ▄█
HBS_TEMPLATE_FILE = "springy.hbs"
HBS_OUTPUT_FILE = "springy.html"

with open(HBS_TEMPLATE_FILE, "r", encoding="utf-8") as file:
    source = file.read()

compiler = Compiler()
template = compiler.compile(source)

output = template(graph)

with open(HBS_OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(output)

# █ █▀▀ █▀█ ▄▀█ █▀█ █ █
# █ █▄█ █▀▄ █▀█ █▀▀ █▀█

g = ig.load("./graph.gml")

style = {}
style["vertex_size"] = 20
style["vertex_color"] = ["#206B61" for v in g.vs]
style["vertex_label"] = ["\n".join(wrap(l, width=30)) for l in g.vs["label"]]
style["vertex_label_dist"] = [1 for v in g.vs]
style["vertex_label_size"] = [16 for v in g.vs]
style["vertex_label_color"] = ["#ffffff" for v in g.vs]
style["edge_width"] = [1 for e in g.es]

random.seed(28975412)

ig.plot(
    g,
    "graph_circle.svg",
    **style,
    layout=g.layout("circle"),
    background="#E73A52",
    bbox=(3000, 3000),
    margin=200,
)


for size in [(3000, 3000), (1500, 3000), (3000, 1500)]:
    ig.plot(
        g,
        f"graph_fruchterman_reingold_{'x'.join(str(s) for s in size)}.svg",
        **style,
        layout=g.layout("fr"),
        background="#E73A52",
        bbox=size,
        margin=200,
    )
