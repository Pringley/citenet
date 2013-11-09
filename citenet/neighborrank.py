import networkx as nx
from citenet import util

def neighborrank(graph, n=100, neighborhood_depth=2):
    """Compute the NeighborRank of the top n nodes in graph, using the
    specified neighborhood_depth."""
    # Get top n nodes with highest outdegree (most often cited).
    nodes = util.top_n_from_dict(graph.out_degree(), n=n)

    # Find neighborhood sizes.
    nhood_sizes = {}
    for root in nodes:
        # Neighborhood begins with just the root.
        nhood = set([root])
        # Expand the neighborhood repeatedly until the depth is reached.
        for i in range(neighborhood_depth):
            prev_nhood = nhood.copy()
            for node in prev_nhood:
                nhood |= set(graph.predecessors(node))
        # Update the results dict.
        nhood_sizes[root] = len(nhood)

    return nhood_sizes
