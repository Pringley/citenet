"""Reports on graph data and metadata."""

from citenet.util import sort_rows

def metadata_histogram(graph, field):
    counts = Counter((graph[node][field]
                      if field in graph[node]
                      else None)
                     for node in graph.nodes())
    header = (field, 'count')
    rows = sort_rows(counts.items())
    return header, rows
