"""Reports on graph data and metadata."""

import numpy as np

from collections import defaultdict, Counter
from citenet.util import sort_rows
from math import floor
from datetime import datetime, date

def date_histogram(graph, date_field, date_format, bins):
    date_fields = (
        graph.node[node][date_field]
        for node in graph.nodes()
        if date_field in graph.node[node]
            and graph.node[node][date_field]
    )
    dates = [
        datetime.strptime(date_str, date_format).timestamp()
        for date_str in date_fields
    ]
    histogram, bin_edges = np.histogram(dates, bins=bins)
    isoedges = [date.fromtimestamp(ts).isoformat() for ts in bin_edges]
    date_ranges = [
        '{} to {}'.format(isoedges[i], isoedges[i+1])
        for i in range(len(isoedges)-1)
    ]
    header = ('date range', 'count')
    rows = zip(date_ranges, histogram)
    return header, rows

def citation_histogram(graph, date_field, date_format, bins):
    date_fields = (
        graph.node[node][date_field]
        for node in graph.nodes()
        if date_field in graph.node[node]
            and graph.node[node][date_field]
    )
    dates = sorted([
        datetime.strptime(date_str, date_format).timestamp()
        for date_str in date_fields
    ])
    histogram, bin_edges = np.histogram(dates, bins=bins)
    isoedges = [date.fromtimestamp(ts).isoformat() for ts in bin_edges]
    date_ranges = [
        '{} to {}'.format(isoedges[i], isoedges[i+1])
        for i in range(len(isoedges)-1)
    ]
    bin_cite_counts = [0 for _ in range(len(histogram))]
    for node in graph.nodes():
        date_str = graph.node[node].get(date_field, None)
        if not date_str:
            continue
        ts = datetime.strptime(date_str, date_format).timestamp()
        bini = 0
        while ts > bin_edges[bini+1]:
            bini += 1
        bin_cite_counts[bini] += len(graph.predecessors(node))
    header = ('date range', 'count', 'total citations made')
    rows = zip(date_ranges, histogram, bin_cite_counts)
    return header, rows

def normalized_outdegree_by_date_and_metadata(graph, 
                                              field,
                                              date_field,
                                              date_format,
                                              bins):
    companies = defaultdict(list)
    for node in graph.nodes():
        key = graph.node[node].get(field, None)
        date_str = graph.node[node].get(date_field, None)
        if not date_str:
            continue
        ts = datetime.strptime(date_str, date_format).timestamp()
        companies[key].append((ts, node))
    header = (
        'company', 'partition', 'start',
        'end', 'normalized outdegree',
        'count', 'total count'
    )
    rows = []
    for company, patents_by_date in companies.items():
        patents_by_date.sort()
        if len(patents_by_date) < bins:
            continue
        bin_size = len(patents_by_date) // bins
        bin_extra = len(patents_by_date) % bins
        partitions = [
            patents_by_date[i:i+bin_size]
            for i in range(0, len(patents_by_date)-bin_extra, bin_size)
        ]
        if bin_extra:
            partitions[-1].extend(patents_by_date[-bin_extra:])
        partition_counts = [
            sum(len(graph.successors(node)) for ts, node in partition)
            for partition in partitions
        ]
        for i in range(len(partitions)):
            rows.append((
                company,
                i,
                date.fromtimestamp(partitions[i][0][0]).isoformat(),
                date.fromtimestamp(partitions[i][-1][0]).isoformat(),
                partition_counts[i] / len(partitions[i]),
                len(partitions[i]),
                len(patents_by_date)
            ))
    return header, sort_rows(rows, column=header.index('total count'))

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
