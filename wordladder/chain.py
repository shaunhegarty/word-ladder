#!/usr/bin/env python

""" Takes two words as arguments and finds the shortest path between them"""

import sys
import logging
from graph import Graph
from ladder import WordLadder

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    """Takes two words as arguments and finds the shortest path between them"""
    ladder = WordLadder()
    # ladder.get_ladder(sys.argv[1],sys.argv[2])
    graph = Graph(ladder.get_graph(len(sys.argv[1])))
    try:
        paths = graph.get_shortest_paths(sys.argv[1], sys.argv[2])
        for path in paths:
            print(f"{path}")
    except KeyError:
        logger.error('One or both words are not in the dictionary')



if __name__ == "__main__":
    main()
