"""Command-line interface for citenet."""

import sys
import json
import os.path
import citenet

def main():
    """Run the CLI."""
    if len(sys.argv) != 2:
        print("Usage: {} <config_file>")

    with open(sys.argv[1]) as config_file:
        config = json.load(config_file)

    graph = citenet.read_csv_graph_and_metadata(config['graph'],
                                                config['metadata'])
    for report_config in config['reports']:
        if (config['options']['cache_reports']
                and os.path.exists(report_config['output'])):
            continue

        function_name = report_config['function']
        function = getattr(citenet.reports, function_name)
        header, rows = function(graph, **report_config['options'])
        delimiter = report_config['delimiter']

        with open(report_config['output'], 'w',
                  encoding=report_config['encoding']) as report_file:
            report_file.write(delimiter.join(header) + '\n')
            for row in rows:
                report_file.write(delimiter.join(map(str, row)) + '\n')
