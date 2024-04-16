import csv
import sys
import json
import networkx as nx
from networkx import NetworkXNoPath

from ladder import WordLadder


class LadderJsonBuilder:
    """Utility Class to build up word ladder data"""

    def __init__(self, word_length: int, top_n: int = 100):
        self.word_length = word_length
        self.dictionary = (
            "common"  # Until we have other word frequency lists, it's always common
        )
        self.dictionary_location = "resources/common.frequency.csv"
        self.top_n = top_n  # We'll use top_n words by frequency (start and end points only, whole list is used in the graph)

    def common_words_by_length_and_frequency(self):
        with open(self.dictionary_location, "r", encoding="utf-8") as dictionary:
            reader = csv.reader(dictionary, delimiter=" ")
            wordlist = [
                (word, int(frequency))
                for word, frequency in reader
                if len(word) == self.word_length
            ]
            wordlist = sorted(wordlist, key=lambda x: x[1], reverse=True)
            return [word for word, _ in wordlist]

    def build_ladder_json(self):
        words = self.common_words_by_length_and_frequency()[: self.top_n]
        word_pairs = self.get_word_pairs(words)
        wordladders = self.get_word_ladders(word_pairs)
        self.write_to_json(wordladders)

    def get_word_pairs(self, words):
        """Get the pairs of words which are sufficiently different enough to be worth looking at the path"""
        word_pairs = set()
        for start_word in words:
            for end_word in words:
                if WordLadder.get_distance(start_word, end_word) > self.word_length - 1:
                    word_pairs.add((start_word, end_word))
        return word_pairs

    def get_word_ladders(self, word_pairs):
        count = 0
        total = len(word_pairs)
        wordladders = {}
        graph = nx.DiGraph(WordLadder(self.dictionary).get_graph(self.word_length))
        for start_word, end_word in word_pairs:
            count += 1
            try:
                shortest_paths = list(
                    nx.all_shortest_paths(graph, start_word, end_word)
                )
                if shortest_paths and len(shortest_paths[0]) > self.word_length - 1:
                    wordladders[(start_word, end_word)] = shortest_paths
            except NetworkXNoPath:
                pass
            if count % 1000 == 0:
                sys.stdout.write(
                    f"\r{count} out of {total} pairs done. Found {len(wordladders.keys())} paths"
                )
                sys.stdout.flush()
        return wordladders

    def write_to_json(self, wordladders):
        ladder_dict = {f"{k[0]}-{k[1]}": v for k, v in wordladders.items()}
        filename = f"resources/ladder-{self.dictionary}-{self.word_length}.json"
        json.dumps(ladder_dict)
        with open(filename, "w", encoding="utf-8") as output:
            output.write(json.dumps(ladder_dict))


if __name__ == "__main__":
    assert sys.argv[1] is not None
    input_word_length = int(sys.argv[1])
    top_n_words = int(sys.argv[2]) if len(sys.argv) >= 3 else 100
    LadderJsonBuilder(
        word_length=input_word_length, top_n=top_n_words
    ).build_ladder_json()
