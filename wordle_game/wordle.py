""" Implement Wordle game.

__version__ = '0.1'
__author__ = 'Adnan Haque'
"""

from typing import List

from colorama import Fore, Style, Back
from pathlib import Path
from bisect import bisect_left
import os.path

import re
import numpy as np

from collections import Counter


# Number of wordle guesses
NUM_GUESSES = 6
ANSWERS_PATH = os.path.join(Path(__file__).parent, '..', 'data/', 'wordle-answers-alphabetical.txt')
GUESS_PATH = os.path.join(Path(__file__).parent, '..', 'data/', 'wordle-allowed-guesses.txt')

EMPTY = -1
GREY = 0
YELLOW = 1
GREEN = 2

WIN = 1
LOSE = 0
IN_PROGRESS = -1

MAX_GUESSES = 6
WORD_LEN = 5


def load_dict(path: str) -> List[str]:
    """Load dictionary of words from file.
    """
    with open(path) as f:
        text = f.read()

    lines = text.splitlines()
    lines = list(filter(lambda x: re.match('^[a-z]{5}$', x), lines))

    return lines


class WordList():
    """Manage dictionary of possible words.
    """

    acceptable_guesses = []
    answers = []

    def __init__(self) -> None:
        self.acceptable_guesses = load_dict(GUESS_PATH)
        self.answers = load_dict(ANSWERS_PATH)

        # Sort for bisection algorithm in future lookups. 
        self.answers = sorted(self.answers)
        self.acceptable_guesses = sorted(self.acceptable_guesses + self.answers)

    def word_index(self, lookup: str) -> int:
        x = bisect_left(self.acceptable_guesses, lookup)

        # Handle if word is not in list
        if self.acceptable_guesses[x] != lookup:
            x = -1
        return x

    def random_guess(self):
        return self.acceptable_guesses[np.random.randint(len(self.answers))]

    def random_target(self):
        return self.answers[np.random.randint(len(self.answers))]

    def valid_guess(self, word) -> bool:
        if len(word) != WORD_LEN:
            return False

        if self.word_index(word) == -1:
            return False

        return True


class WordleGame():

    state = None
    wordlist = None
    target = None
    round = 1
    guesses = []

    def __init__(self, wordlist: WordList = WordList(), target=None) -> None:
        self.wordlist = wordlist
        self.state = np.empty(shape=(MAX_GUESSES, WORD_LEN), dtype=int)
        self.state.fill(EMPTY)
        self.guesses = []
        self.round = 1

        if target is None:
            self.target = wordlist.random_target()
        else:
            self.target = target

    def guess(self, word: str) -> bool:
        if not self.wordlist.valid_guess(word):
            return False

        # Update state
        self.state[self.round - 1, :] = generate_state(self.target, word)
        self.round += 1
        self.guesses.append(word)
        return True

    def add_state(self, guess, state_str: str) -> None:
        """Update game with current state, designed for external play.
        """
        self.guesses.append(guess)

        for i, c in enumerate(state_str):
            state = EMPTY
            if c == "B":
                state = GREY
            elif c == "G":
                state = GREEN
            elif c == "Y":
                state = YELLOW

            self.state[self.round - 1, i] = state

        self.round += 1

    def complete(self) -> int:
        """Determine if game is complete.
        """
        if np.all(self.state[self.round - 2, :] == GREEN):
            return WIN

        if self.round > MAX_GUESSES:
            return LOSE

        return IN_PROGRESS 

    def __str__(self):

        def transform_char(x: int, input_string) -> str:
            if x == GREY:
                val = Back.BLACK + Fore.WHITE
            elif x == GREEN:
                val = Back.GREEN + Fore.WHITE
            elif x == YELLOW:
                val = Back.YELLOW + Fore.WHITE
            else:
                val = Back.WHITE

            val = val + input_string.upper() + Style.RESET_ALL
            return val

        output = ""
        _, M = self.state.shape
        for i in range(len(self.guesses)):
            for j in range(M):
                output += transform_char(self.state[i, j], self.guesses[i][j])
            output += "\n"
        return output


def valid_state(input: str) -> bool:
    """Return if string representation of state is valid.
    """
    return bool(re.match('^[GYB]{5}$', input))


def generate_state(target, word):
    """Generate state of guess.

    Examples
    --------
    >>> np.all(generate_state("raise", "paire") == np.array([GREY, GREEN, GREEN, YELLOW, GREEN]))
    True
    >>> np.all(generate_state("boils", "loops") == np.array([YELLOW, GREEN, GREY, GREY, GREEN]))
    True
    >>> np.all(generate_state("flute", "belle") == np.array([GREY, GREY, YELLOW, GREY, GREEN]))
    True
    """
    target_counter = Counter(target)
    state = np.empty(WORD_LEN, dtype=int)
    for i, char in enumerate(word):
        if char == target[i]:
            state[i] = GREEN
            target_counter[char] -= 1

    for i, char in enumerate(word):
        if char == target[i]:
            continue
        elif target_counter[char] > 0:
            state[i] = YELLOW
        else:
            state[i] = GREY
            continue
        target_counter[char] -= 1
    return state