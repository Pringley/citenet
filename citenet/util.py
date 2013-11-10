"""Utility functions for citenet."""

def top_n_from_dict(dictionary, amount):
    """Get the top ``amount`` keys from ``dictionary``, sorted by value."""
    return sorted(dictionary,
                  key=dictionary.__getitem__,
                  reverse=True)[:amount]
