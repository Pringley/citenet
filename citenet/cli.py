"""Command-line interface for citenet."""

import sys
import json
import citenet

def main():
    """Run the CLI."""
    if len(sys.argv) != 2:
        print("Usage: {} <config_file>")

    with open(sys.argv[1]) as config_file:
        config = json.load(config_file)

    graph = citenet.read_csv_graph(**config['graph'])
