"""Module implementing all solvers of Wordle.
"""

from typing import List
from collections import Counter

import wordle
import numpy as np


class BaseSolver():
    """Base Wordle solver.
    """

    word_list = None
    first_guess = "raise"

    def guess(self, game: wordle.WordleGame):
        raise NotImplementedError("Not implemented!")

    def simulate_game(self, game) -> int:
        """Simulate game and return rounds to win.
        """
        round = game.round - 1

        while game.complete() == wordle.IN_PROGRESS:
            guess = self.guess(game)
            game.guess(guess)
            round += 1

        return round

    def simulate(self, game) -> List[int]:
        """Simulate game and return distribution of wins.
        """
        round = game.round - 1

        while game.complete() == wordle.IN_PROGRESS:
            guess = self.guess(game)
            game.guess(guess)
            round += 1

        return round


def filter_answers(game):
    """Filter answers.
    """
    guess_list = game.wordlist.answers
    _, M = game.state.shape
    for i in range(game.round - 1):

        # Handle words with multiple of the same letter.
        letter_dist = Counter()
        for j in range(M):
            letter = game.guesses[i][j]
            if letter_dist[letter] > 0:
                continue
            state = game.state[i, j]
            if state == wordle.GREY:
                guess_list = filter(lambda word: letter not in word, guess_list)
            elif state == wordle.YELLOW:
                guess_list = filter(lambda word: letter in word, guess_list)
            elif state == wordle.GREEN:
                guess_list = filter(lambda word: letter == word[j], guess_list)
            guess_list = list(guess_list)
            letter_dist[letter] += 1

    guess_list = list(guess_list)
    return guess_list


class RandomSolver(BaseSolver):
    """Naive solution.
    """

    def __init__(self, word_list=wordle.WordList()):
        self.word_list = word_list
        self.guess_list = word_list.answers

    def guess(self, game: wordle.WordleGame):
        if game.round == 1:
            return self.first_guess

        guess_list = self.word_list.answers
        guess_list = filter_answers(game)

        if len(guess_list) == 0:
            raise ValueError("No valid guesses left!")
        # return guesses[np.random.randint(len(guesses))]
        return guess_list[0]