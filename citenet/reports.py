"""Reports on graph data and metadata."""

from collections import defaultdict, Counter
from citenet.util import sort_rows
from math import floor

def metadata_histogram(graph, field):
    counts = Counter((graph.node[node][field]
                      if field in graph.node[node]
                      else None)
                     for node in graph.nodes())
    header = (field, 'count')
    rows = sort_rows(counts.items())
    return header, rows

def normalized_outdegree_by_metadata(graph, field):
    histogram = Counter(graph.node[node].get(field, None)
                        for node in graph.nodes())
    counts = defaultdict(int)
    for node in graph.nodes():
        key = graph.node[node].get(field, None)
        counts[key] += len(graph.successors(node))

    rows = sort_rows((field, degree / histogram[field], degree, histogram[field])
                     for field, degree in counts.items())
    header = (field, 'normalized outdegree', 'summed outdegree', 'total patents')
    return header, rows

def good_outdegree_ratio_by_metadata(graph, field, ratio_cutoff):
    histogram = Counter(graph.node[node].get(field, None)
                        for node in graph.nodes())
    all_outdegrees = sorted((len(graph.successors(node))
                             for node in graph.nodes()),
                            reverse=True)
    cutoff = all_outdegrees[floor(len(all_outdegrees)*ratio_cutoff)]
    counts = {key: 0 for key in histogram.keys()}
    for node in graph.nodes():
        key = graph.node[node].get(field, None)
        if len(graph.successors(node)) >= cutoff:
            counts[key] += 1
    rows = sort_rows(((field, count / histogram[field], histogram[field], count)
                      for field, count in counts.items()), column=2)
    header = (field, 'significance fraction',
              'total number of patents',
              'number of patents with outdegree >= {}'.format(cutoff))
    return header, rows

def outdegree_histogram(graph):
    histogram = Counter(len(graph.successors(node)) for node in graph.nodes())
    header = ('outdegree', 'count')
    rows = sort_rows(histogram.items())
    return header, rows
