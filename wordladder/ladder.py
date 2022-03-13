#!/usr/bin/env python

import sys
import pickle
import os.path
import logging
from graph import Graph
from ladderdata import LadderData

logger = logging.getLogger(__name__)


class WordLadder:
    RESOURCE_LOCATION = "resources/"
    WEBSTER_LOCATION = RESOURCE_LOCATION + "websters-dictionary.txt"
    SOWPODS_LOCATION = RESOURCE_LOCATION + "sowpods.txt"
    WEBSTER = "webster"
    SOWPODS = "sowpods"
    FILE_END = "gra.ph"

    use_webster = 1
    file_suffix = SOWPODS + FILE_END

    def __init__(self, use_webster):
        """Initialises the word ladder object, taking a boolean as a parameter
        to decide the dictionary to use"""
        if use_webster is None:
            use_webster = False
        self.use_webster = use_webster

        if use_webster:
            self.file_suffix = self.WEBSTER + self.FILE_END
            logger.info(self.file_suffix)

    def get_word_list(self, word_length, include_proper_nouns=False):
        dictionary_path = self.SOWPODS_LOCATION
        if self.use_webster:
            dictionary_path = self.WEBSTER_LOCATION

        # Read the words of the correct length from the dictionary and add
        # them to a list. Exclude proper nouns
        with open(dictionary_path, "r", encoding="utf-8") as dictionary:
            wordlist = []
            for line in dictionary:
                line = line.strip()
                if len(line) == word_length and (
                    include_proper_nouns or line.lower() == line
                ):
                    wordlist.append(line)
        return wordlist

    def get_ladder(self, start, end):

        start = start.strip().lower()
        end = end.strip().lower()
        if len(start) != len(end):
            logger.error("Arguments must be two words of the same length")
            return

        # Read the words of the correct length from the dictionary and add them to a list
        graph = Graph(self.get_graph(len(start)))

        # show that the program did something
        path = graph.get_shortest_path(start, end)
        logger.info(path)

    def get_ladder_from_scratch(self, start, end):

        start = start.strip().lower()
        end = end.strip().lower()
        assert len(start) != len(end), "Arguments must be two words of the same length"

        # Read the words of the correct length from the dictionary and add them to a list
        word_length = len(start)
        wordlist = self.get_word_list(word_length)
        graph = Graph(self.build_graph(wordlist))

        # show that the program did something
        path = graph.get_shortest_path(start, end)
        logging.info(path)
        return path

    def is_one_away(self, first_word: str, second_word: str):
        """returns true if the two words differ by exactly one letter"""
        return self.get_distance(first_word, second_word) == 1

    @staticmethod
    def get_distance(first_word: str, second_word: str):
        """Get the letter distance between the two words"""
        diff_count = 0
        # both words should be same length at this point
        for index in range(0, len(first_word)):
            if first_word[index : index + 1] != second_word[index : index + 1]:
                diff_count = diff_count + 1
        return diff_count

    def save_graph(self, word_length: int):
        graph = self.build_graph(self.get_word_list(word_length))
        filename = self.RESOURCE_LOCATION + str(word_length) + self.file_suffix
        with open(filename, "wb") as output:
            pickle.dump(graph, output, pickle.HIGHEST_PROTOCOL)

    def save_graphs(self):
        min_word_length = 2
        max_word_length = 8
        for word_length in range(min_word_length, max_word_length):
            self.save_graph(word_length)

    def load_graph(self, word_length):
        filename = self.RESOURCE_LOCATION + str(word_length) + self.file_suffix
        with open(filename, "rb") as input_file:
            graph = pickle.load(input_file)

        return graph

    # Try to build a graph of the whole thing
    def build_graph(self, wordlist):
        graph = {}
        count = 0
        for word in wordlist:
            graph[word] = self.get_neighbour_list(word, wordlist)
            count = count + 1
            if count % 10 == 0:
                sys.stdout.write(f"\r{count} out of {len(wordlist)} nodes done")
                sys.stdout.flush()
        return graph

    def get_graph(self, word_length):
        fname = self.RESOURCE_LOCATION + str(word_length) + self.file_suffix
        if not os.path.isfile(fname):
            self.save_graph(word_length)
        return self.load_graph(word_length)

    # get list of neighbours
    def get_neighbour_list(self, word, wordlist):
        neighbour_list = []
        for neighbour in wordlist:
            if self.is_one_away(word, neighbour):
                neighbour_list.append(neighbour)
        return neighbour_list

    def get_ladder_data(self, word):
        fname = "words/" + word + self.file_suffix
        if not os.path.isfile(fname):
            self.build_ladder_data(word)
        data = self.load_ladder_data(word)

        return data

    def load_ladder_data(self, word):
        filename = "words/" + word + self.file_suffix
        with open(filename, "rb") as input_file:
            data = pickle.load(input_file)

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
            sys.stdout.write(
                f"\r{count} out of {len(wordlist)} paths done: {word} to {target}"
            )
            sys.stdout.flush()
            path = graph.get_shortest_path(word, target)
            data.add_path(path)

        filename = word + self.file_suffix

        with open("words/" + filename, "wb") as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
        return data
