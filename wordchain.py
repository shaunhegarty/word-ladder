#!/usr/bin/env python

import sys
import pickle
import os.path
from wordgraph import Graph
from wordladder import WordLadder

#main function
def main():

    if len(sys.argv) != 3:
        print 'Needs exactly 3 arguments'
        return
    
    ladder = WordLadder(False)
    ladder.get_ladder(sys.argv[1],sys.argv[2])
        

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()



