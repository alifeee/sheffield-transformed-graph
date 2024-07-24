"""Render the graph.yaml into a webpage"""
import yaml
from pybars import Compiler

INPUT_FILE = "graph.yaml"
TEMPLATE_FILE = "index.hbs"
OUTPUT_FILE = "index.html"

with open(TEMPLATE_FILE, 'r', encoding="utf-8") as file:
    source = file.read()

with open(INPUT_FILE, 'r', encoding="utf-8") as file:
    graph = yaml.safe_load(file)

# make edges into objects
graph["edges"] = [edge.split(", ") for edge in graph["edges"]]

# error if any edges do not exist
for edge in graph["edges"]:
    if edge[0] not in graph["nodes"] or edge[1] not in graph["nodes"]:
        raise ValueError(f"{edge[0]} or {edge[1]} are not nodes")

compiler = Compiler()
template = compiler.compile(source)

output = template(graph)

with open(OUTPUT_FILE, 'w', encoding="utf-8") as file:
    file.write(output)
