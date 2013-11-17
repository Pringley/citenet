"""Command-line interface for citenet."""

import sys
import json
import code
import os.path
import logging
import citenet

LOGGING_FORMAT = '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'

def main():
    """Run the CLI."""
    logger = logging.getLogger(__name__)

    if '-v' or '--verbose' in sys.argv:
        loglevel = logging.DEBUG
    elif '-q' or '--quiet' in sys.argv:
        loglevel = logging.CRITICAL
    else:
        loglevel = logging.INFO

    positional_args = [
        arg
        for arg in sys.argv[1:]
        if not arg.startswith('-')
    ]

    if len(positional_args) != 2:
        print("Usage: {} [options] reports <config_file>")
        print("       {} [options] interact <config_file>")

    command = positional_args[0]
    config_filename = positional_args[1]

    logging.basicConfig(level=logging.INFO,
                        format=LOGGING_FORMAT)

    with open(config_filename) as config_file:
        config = json.load(config_file)

    graph = citenet.read_csv_graph_and_metadata(config['graph'],
                                                config['metadata'])
    if command == 'reports':
        generate_reports(graph, config)
    elif command == 'interact':
        code.interact(
            local={
                'graph': graph,
                'config': config,
                'logger': logger
            },
            banner="Welcome to CiteNet! Your data is loaded in ``graph``."
        )

def generate_reports(graph, config):
    """Generate reports specified in config."""
    logger = logging.getLogger(__name__)
    for report_config in config['reports']:
        if (config['options']['cache_reports']
                and os.path.exists(report_config['output'])):
            logger.debug('Skipping completed report: {}'
                         .format(report_config['output']))
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

        logger.info('Generated report: {}'.format(report_config['output']))
