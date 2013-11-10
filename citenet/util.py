"""Utility functions for citenet."""

from operator import itemgetter

def sort_rows(rows, column=1, highest_first=True):
    """Sort rows by a specified column.

    Parameters:
        rows -- a sequence of sequences representing table rows
        column -- an integer specifying which column to sort by
        highest_first -- optional flag specifying descending order (True)

    """
    return sorted(rows,
                  key=itemgetter(column),
                  reverse=highest_first)

def top_n_from_dict(dictionary, amount):
    """Get the top ``amount`` keys from ``dictionary``, sorted by value."""
    return sort_rows(dictionary.items())[:amount]
