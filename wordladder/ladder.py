#!/usr/bin/env python

import sys
import pickle
import os.path
import logging
import csv
import string

from dataclasses import dataclass

from graph import Graph
from ladderdata import LadderData

logger = logging.getLogger(__name__)


@dataclass
class WordList:
    """Class for word lists"""

    name: str
    filename: str
    resource_location: str = "resources/"
    is_csv: bool = False

    @property
    def location(self) -> str:
        return os.path.join(self.resource_location, self.filename)

    @property
    def file_suffix(self) -> str:
        return f"{self.name}gra.ph"

    def __str__(self):
        return f"{self.name}: {self.filename}"


class WordLadder:
    WORDLISTS = {
        "sowpods": WordList("sowpods", "sowpods.txt"),
        "webster": WordList("webster", "websters-dictionary.txt"),
        "common": WordList("common", "common.frequency.csv", is_csv=True),
    }

    def __init__(self, word_list="common"):
        """Initialises the word ladder object, taking a boolean as a parameter
        to decide the dictionary to use"""
        self.dictionary = WordLadder.WORDLISTS.get(word_list)

    def get_word_list(self, word_length, include_proper_nouns=False):
        dictionary_path = self.dictionary.location

        # Read the words of the correct length from the dictionary and add
        # them to a list. Exclude proper nouns
        with open(dictionary_path, "r", encoding="utf-8") as dictionary:
            if self.dictionary.is_csv:
                reader = csv.reader(dictionary, delimiter=" ")
                wordlist = {word for word, _ in reader if len(word) == word_length}
            else:
                wordlist = set()
                for line in dictionary:
                    line = line.strip()
                    if len(line) == word_length and (
                        include_proper_nouns or line.lower() == line
                    ):
                        wordlist.add(line)
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
        assert len(start) == len(
            end
        ), f"Arguments must be two words of the same length: {start}, {end} "

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
        filename = f"{self.dictionary.resource_location}{word_length}{self.dictionary.file_suffix}"
        with open(filename, "wb") as output:
            pickle.dump(graph, output, pickle.HIGHEST_PROTOCOL)

    def save_graphs(self):
        min_word_length = 2
        max_word_length = 8
        for word_length in range(min_word_length, max_word_length):
            self.save_graph(word_length)

    def load_graph(self, word_length):
        filename = f"{self.dictionary.resource_location}{word_length}{self.dictionary.file_suffix}"
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
        filename = f"{self.dictionary.resource_location}{word_length}{self.dictionary.file_suffix}"
        if not os.path.isfile(filename):
            self.save_graph(word_length)
        return self.load_graph(word_length)

    # get list of neighbours
    def get_neighbour_list(self, word, wordlist):
        neighbour_list = set()
        for index in range(len(word)):
            for letter in string.ascii_lowercase:
                neighbour_word = word[:index] + letter + word[index + 1 :]
                if neighbour_word in wordlist:
                    neighbour_list.add(neighbour_word)
        neighbour_list.remove(word)
        return list(neighbour_list)

    def get_ladder_data(self, word):
        fname = "words/" + word + self.dictionary.file_suffix
        if not os.path.isfile(fname):
            self.build_ladder_data(word)
        data = self.load_ladder_data(word)

        return data

    def load_ladder_data(self, word):
        filename = "words/" + word + self.dictionary.file_suffix
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

        filename = word + self.dictionary.file_suffix

        with open("words/" + filename, "wb") as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
        return data
