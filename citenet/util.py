def top_n_from_dict(d, n):
    """Get the top n keys from dictionary d, sorted by value."""
    return sorted(d, key=d.__getitem__, reverse=True)[:n]
