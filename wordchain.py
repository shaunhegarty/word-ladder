#!/usr/bin/env python

import sys
from wordgraph import Graph
from wordladder import WordLadder


def main():

    #    if len(sys.argv) != 3:
    #       print 'Needs exactly 3 arguments'
    #       return

    ladder = WordLadder(False)
    # ladder.get_ladder(sys.argv[1],sys.argv[2])
    g = ladder.get_graph(len(sys.argv[1]))
    graph = Graph(g)
    paths = graph.get_shortest_paths(sys.argv[1], sys.argv[2])
    for path in paths:
        print("\n" + str(path))


if __name__ == "__main__":
    main()
