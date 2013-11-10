"""Utilities for reading and writing citation graphs."""

import csv
import logging
from networkx import DiGraph

def read_csv_graph(filename,
                   delimiter=',',
                   reverse_edges=False,
                   suppress_warnings=False,
                   ignore_header=False):
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
    with open(filename, newline='') as file_obj:
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
