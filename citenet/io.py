"""Utilities for reading and writing citation graphs."""

import csv
import logging
from networkx import DiGraph

def read_csv_graph_and_metadata(graph_cfg, metadata_cfgs):
    """Read a graph with metadata."""

    logger = logging.getLogger(__name__)

    graph = read_csv_graph(**graph_cfg)

    for metadata_cfg in metadata_cfgs:
        metadata = read_csv_metadata(**metadata_cfg)
        for node, fields in metadata.items():
            for key, val in fields.items():
                try:
                    graph[node][key] = val
                except KeyError:
                    if not metadata_cfg.get('suppress_warnings', False):
                        logger.warn('Metadata node {} not found'.format(node))

    return graph

def read_csv_graph(filename,
                   delimiter=',',
                   encoding=None,
                   reverse_edges=False,
                   suppress_warnings=False,
                   ignore_header=True):
    """Read an edgelist style graph from a CSV file.

    Options:
        filename -- path to the csv file
        delimiter -- CSV delimiter (e.g. ',', '\\t')
        reverse_edges -- flag if edges aren't in (source, dest) order
        suppress_warnings -- flag to ignore "bad line" warnings
        ignore_header -- flag to ignore the first line in CSV file

    """
    logger = logging.getLogger(__name__)

    edgeset = set()
    with open(filename, encoding=encoding, newline='') as file_obj:
        reader = csv.reader(file_obj, delimiter=delimiter)

        # Skip header line (if specified).
        if ignore_header:
            _ = next(reader)

        for row in reader:
            pair = tuple(row if not reverse_edges
                         else reversed(row))

            def warn(message):
                """Log a warning on this line."""
                if suppress_warnings:
                    return
                full_message = 'Error in {} on line {}: {}'
                logger.warn(full_message.format(filename,
                                                reader.line_num,
                                                message))

            if not all(pair):
                warn('Incomplete edge: {}'.format(pair))
            elif pair in edgeset:
                warn('Duplicate edge: {}'.format(pair))
            else:
                # If no errors, add the edge!
                edgeset.add(pair)

    graph = DiGraph()
    graph.add_edges_from(edgeset)

    return graph

def read_csv_metadata(filename,
                      delimiter=',',
                      encoding=None,
                      suppress_warnings=False,
                      id_field='id'):
    """Read metadata from a CSV file.

    Options:
        filename -- path to the csv file
        delimiter -- CSV delimiter (e.g. ',', '\\t')
        suppress_warnings -- flag to ignore "bad line" warnings
        id_field -- name of field identifying the node

    """
    metadata = {}
    with open(filename, encoding=encoding, newline='') as file_obj:
        reader = csv.reader(file_obj, delimiter=delimiter)

        header = next(reader)

        for row in reader:
            fields = dict(zip(header, row))
            key = fields[id_field]
            del fields[id_field]
            metadata[key] = fields

    return metadata
