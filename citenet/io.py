"""Utilities for reading and writing citation graphs."""

import gzip
from networkx.readwrite import json_graph

def write_json_graph(graph, filename, compressed=True):
    """Write a graph to file."""
    if compressed:
        file_obj = gzip.open(filename, 'wb')
    else:
        file_obj = open(filename, 'w')
    try:
        json_graph.dump(graph, file_obj)
    finally:
        file_obj.close()

def read_json_graph(filename, compressed=True):
    """Read a graph from file."""
    if compressed:
        file_obj = gzip.open(filename, 'rb')
    else:
        file_obj = open(filename)
    try:
        graph = json_graph.load(file_obj)
    finally:
        file_obj.close()
    return graph
