#!/usr/bin/env python

import sys
import pickle
import os.path
from wordgraph import Graph
from wordladderdata import LadderData

class WordLadder(object):
    RESOURCE_LOCATION = "resources/"
    WEBSTER_LOCATION = RESOURCE_LOCATION + "websters-dictionary.txt"
    SOWPODS_LOCATION = RESOURCE_LOCATION + "sowpods.txt"
    WEBSTER = "webster"
    SOWPODS = "sowpods"
    FILE_END = "gra.ph"
    
    use_webster = 1
    file_suffix = SOWPODS + FILE_END
    
    def __init__(self, use_webster):
        #Initialises the word ladder object, taking a boolean as a parameter to decide the dictionary to use
        if use_webster == None:
            use_webster = False
        self.use_webster = use_webster
        
        if use_webster:
            self.file_suffix = self.WEBSTER + self.FILE_END
            print self.file_suffix

    def get_word_list(self, word_length):
        dictionaryPath = self.SOWPODS_LOCATION
        if self.use_webster:
            dictionaryPath = self.WEBSTER_LOCATION
        

        #Read the words of the correct length from the dictionary and add them to a list
        with open(dictionaryPath, "r") as dictionary:
            wordlist = []
            for line in dictionary:            
                line = line.strip()
                if len(line) == word_length:
                    wordlist.append(line)

        return wordlist

    def get_ladder(self, start, end):
       
        start = start.strip().lower();
        end = end.strip().lower();
        if len(start) != len(end):
            print "Arguments must be two words of the same length"
            return  

        #Read the words of the correct length from the dictionary and add them to a list
        g = self.get_graph(len(start))
        graph = Graph(g)
        
                    
        #show that the program did something
        path = graph.get_shortest_path(start, end)
        print path


    def get_ladder_from_scratch(self, start, end):
       
        start = start.strip().lower();
        end = end.strip().lower();
        if len(start) != len(end):
            print "Arguments must be two words of the same length"
            return  

        #Read the words of the correct length from the dictionary and add them to a list
        word_length = len(start)
        wordlist = get_word_list(word_length)
        graph = Graph(build_graph(wordlist))
        
                    
        #show that the program did something
        path = graph.get_shortest_path(start, end)        
        print path

    #returns true if the two words differ by exactly one letter
    def is_one_away(self, a, b):
        return self.get_distance(a, b) == 1

    #Get the letter distance between the two words
    def get_distance(self, a, b):
        diff_count = 0;
        for x in range (0, len(a)): #a and b should be same length at this point
            if a[x:x+1] != b[x:x+1]:
                diff_count = diff_count + 1                                        
        return diff_count

    def save_graph(self, x):
        graph = self.build_graph(self.get_word_list(x))
        filename = self.RESOURCE_LOCATION + str(x) + self.file_suffix
        with open(filename, 'wb') as output:
            pickle.dump(graph, output, pickle.HIGHEST_PROTOCOL) 

    def save_graphs(self):
        for x in range(2, 8):
            save_graph(x) 

    def load_graph(self, word_length):
        filename = self.RESOURCE_LOCATION + str(word_length) + self.file_suffix
        with open(filename, 'rb') as input:
            graph = pickle.load(input)

        return graph

    #Try to build a graph of the whole thing
    def build_graph(self, wordlist):
        graph = {}
        count = 0;
        for word in wordlist:
            graph[word] = self.get_neighbour_list(word, wordlist)
            count = count + 1
            if count % 10 == 0:
                sys.stdout.write("\r" + str(count) + " out of " + str(len(wordlist)) + " nodes done")
                sys.stdout.flush()      
        return graph

    def get_graph(self, word_length):
        fname = self.RESOURCE_LOCATION + str(word_length) + self.file_suffix
        if not os.path.isfile(fname):
            self.save_graph(word_length)
        return self.load_graph(word_length)
        
    #get list of neighbours
    def get_neighbour_list(self, word, wordlist):
        neighbour_list = []
        for neighbour in wordlist:
            if self.is_one_away(word, neighbour):
                neighbour_list.append(neighbour)
        return neighbour_list

    def get_ladder_data(self, word):
        fname = 'words/' + word + self.file_suffix
        if not os.path.isfile(fname):
            self.build_ladder_data(word)        
        data = self.load_ladder_data(word)
        
        return data

    def load_ladder_data(self, word):
        filename = 'words/' + word + self.file_suffix
        with open(filename, 'rb') as input:
            data = pickle.load(input)

        return data

    def build_ladder_data(self, word):
        wordlist = self.get_word_list(len(word))
        graph = Graph(self.get_graph(len(word)))
        data = LadderData(word)

        count = 0
        for target in wordlist:
            if word == target:
                continue
            count = count + 1
            sys.stdout.write("\r" + str(count) + " out of " + str(len(wordlist)) + " paths done: " + word + " to " + target)
            sys.stdout.flush()   
            path = graph.get_shortest_path(word, target)
            data.add_path(path)

        filename = word + self.file_suffix

        with open('words/' + filename, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL) 
        return data
