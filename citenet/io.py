import gzip
import json
from networkx.readwrite import json_graph

def write_json_graph(graph, filename, compressed=True):
    """Write a graph to file."""
    if compressed:
        fp = gzip.open(filename, 'wb')
    else:
        fp = open(filename, 'w')
    try:
        json_graph.dump(graph, fp)
    finally:
        fp.close()

def read_json_graph(filename, compressed=True):
    """Read a graph from file."""
    if compressed:
        fp = gzip.open(filename, 'rb')
    else:
        fp = open(filename)
    try:
        graph = json_graph.load(fp)
    finally:
        fp.close()
    return graph
