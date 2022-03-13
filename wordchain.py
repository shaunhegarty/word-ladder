#!/usr/bin/env python

""" Takes two words as arguments and finds the shortest path between them"""

import sys
import logging
from wordgraph import Graph
from wordladder import WordLadder

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    """Takes two words as arguments and finds the shortest path between them"""
    ladder = WordLadder(True)
    # ladder.get_ladder(sys.argv[1],sys.argv[2])
    graph = Graph(ladder.get_graph(len(sys.argv[1])))
    paths = graph.get_shortest_paths(sys.argv[1], sys.argv[2])
    for path in paths:
        print(f"{path}")


if __name__ == "__main__":
    main()
