""" This class will store the wordladder data for a given word """
import logging

logger = logging.getLogger(__name__)


class LadderData(object):

    base_word = ""

    # word_data should be filled with paths that exist between
    # base_word and some target word, which should be the key for the path
    word_data = {}

    def __init__(self, word):
        self.base_word = word

    def add_path(self, path):
        if path is None:
            return

        if path[0] != self.base_word:
            logger.error("Invalid path entered")
            return
        # add path as data entry, with end word as the key
        datakey = path[len(path) - 1]
        self.word_data[datakey] = path
