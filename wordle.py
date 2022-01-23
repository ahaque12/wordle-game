""" Play wordle.

__version__ = '0.1'
__author__ = 'Adnan Haque'
"""

from pathlib import Path
import os.path

import re
import numpy as np


# Number of wordle guesses
NUM_GUESSES = 6
ANSWERS_PATH = os.path.join(Path(__file__).parent, 'data/', 'wordle-answers-alphabetical.txt')
GUESS_PATH = os.path.join(Path(__file__).parent, 'data/', 'wordle-allowed-guesses.txt')


class WordleGame():

    state = None

    def __init__(self) -> None:
        pass


class WordList():
    """Manage dictionary of possible words.
    """

    acceptable_guesses = None
    answers = None

    def __init__(self) -> None:
        acceptable_guesses = load_dict(GUESS_PATH)
        answers = load_dict(ANSWERS_PATH)


    def lookup_word(self: WordList, partial_string: str) -> List[str]:
        pass


class WordleSolver():
    """Wordle solver.
    """

    pass


def load_dict(path: str) -> None:
    """Load dictionary of words from file.
    """
    with open(DICT_PATH) as f:
        text = f.read()

    lines = text.splitlines()
    lines = list(filter(lambda x: re.match('^[a-z]{5}$', x), lines))

    words = (lines)

