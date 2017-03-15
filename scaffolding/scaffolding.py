#!/usr/bin/env python
"""
"""

import argparse
import json
import logging
import requests
import sys


logger = logging.getLogger('scaffolding')


def parse_args():
    parser = argparse.ArgumentParser(description="Generic python scaffolding script")
    parser.add_argument('--loglevel', default='INFO', help="Loglevel Default: %(default)r")
    parser.add_argument('--logfile', default='-', help="Logfile location Default: STDOUT")

    return parser.parse_args()


def setup_logging(arguments):
    logger.setLevel(logging.getLevelName(arguments.loglevel.upper()))
    if arguments.logfile == '-':
        ch = logging.StreamHandler()
    else:
        ch = logging.handlers.RotatingFileHandler(arguments.logfile,
                                                  maxBytes=20 * 1024 * 1024,
                                                  backupCount=1)
    formatter = logging.Formatter('%(asctime)s %(levelname)-7s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def main():
    arguments = parse_args()
    setup_logging(arguments)

    logger.info('Starting the loop. Checking {} every {} seconds'.format(
        arguments.server,
        arguments.sleep
    ))

    url = "http://google.com"
    logger.debug("Using URL: {}".format(url))


    try:
        response = requests.get(url, headers={'Accept': 'application/json'}, timeout=10)
    except requests.ConnectionError:
        print 'WARNING:Got ConnectionError'
        sys.exit(1)
    except requests.Timeout:
        print 'WARNING: Got Timeout'
        sys.exit(1)

    try:
        response_dict = json.loads(response.content)
    except ValueError:
        print "CRITICAL: Could not parse the return. {}".format(response.content)
        sys.exit(2)

    print response_dict


if __name__ == '__main__':
    main()
