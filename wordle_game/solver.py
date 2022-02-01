"""Module implementing all solvers of Wordle.
"""

from typing import List
from collections import Counter
import os.path
from pathlib import Path

from wordle_game import wordle, helper
import numpy as np
from tqdm import tqdm

STATE_PATH = os.path.join(Path(__file__).parent, '..', 'data/', 'state_space.npy')


class BaseSolver():
    """Base Wordle solver.
    """

    wordlist = None
    first_guess = "soare"

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

        # Number of rounds is -1 if you lose.
        if game.complete() != wordle.WIN:
            round = -1

        return round

    def simulate(self) -> List[int]:
        """Simulate game and return distribution of rounds to win.
        """

        results = []
        for word in tqdm(self.wordlist.answers):
            results.append(self.simulate_game(wordle.WordleGame(wordlist=self.wordlist, target=word)))

        return np.array(results)


def filter_answers(game) -> List[str]:
    """Filter for potential answers.

    Parameters
    ----------
    game : WordleGame, required
        Game being played.

    Returns
    -------
    filtered_answers : List[str]
        List of possible answers after filtering out
        initial list using the list of guesses and 
        state responses.
    """
    guess_list = game.wordlist.answers
    _, M = game.state.shape
    for i in range(game.round - 1):

        letter_dist = Counter(game.guesses[i])

        # Deal with greens first
        for j in range(M):
            letter = game.guesses[i][j]
            state = game.state[i, j]
            if state == wordle.GREEN:
                guess_list = filter(lambda word: letter == word[j], guess_list)
            guess_list = list(guess_list)

        # Deal with single yellow's and grey's.
        for j in range(M):
            letter = game.guesses[i][j]
            state = game.state[i, j]

            # Handle edge case of multiple of the same letter below.
            if state == wordle.GREEN:
                continue

            if state == wordle.GREY and letter_dist[letter] <= 1:
                guess_list = filter(lambda word: letter not in word, guess_list)
            elif state == wordle.YELLOW:
                guess_list = filter(lambda word: letter in word, guess_list)
                guess_list = filter(lambda word: letter != word[j], guess_list)
            guess_list = list(guess_list)

        # Handle edge case of multiple of the same letter.
        for letter, count in letter_dist.items():
            if count > 1:
                byg_dist = Counter(game.state[i, np.where([x == letter for x in game.guesses[i]])[0]].tolist())
                if byg_dist[wordle.GREY] == 0:
                    pass
                    guess_list = filter(lambda word: Counter(word)[letter] >= byg_dist[wordle.YELLOW] + byg_dist[wordle.GREEN], guess_list)
                else:
                    pass
                    guess_list = filter(lambda word: Counter(word)[letter] == byg_dist[wordle.YELLOW] + byg_dist[wordle.GREEN], guess_list)
                guess_list = list(guess_list)

    return guess_list


class RandomSolver(BaseSolver):
    """Naive solution.

    Randomly select the first potential answer of
    the list of remaining possible answers at each 
    game iteration.
    """

    def __init__(self, wordlist=wordle.WordList()):
        self.wordlist = wordlist

    def guess(self, game: wordle.WordleGame):
        """Determine optimal guess.
        """
        if game.round == 1:
            return self.first_guess

        guess_list = self.wordlist.answers
        guess_list = filter_answers(game)

        if len(guess_list) == 0:
            raise ValueError("No valid guesses left!")
        # return guesses[np.random.randint(len(guesses))]
        return guess_list[0]


def convert_state(state: np.ndarray):
    """Convert state to unique numerical representation for performance.

    Given each digit can be in one of three states each individual state 
    response can be represented by a ternary number.
    """
    return state[0]+state[1]*3+state[2]*9+state[3]*27+state[4]*81


class MaxEntropy(BaseSolver):
    """Maximize entropy.

    Determine optimal next guess by maximizing entropy of each guess.
    Entropy is maximized by having as close to uniform a distribution of 
    possible answers across unique state responses.
    """

    def __create_state_space(self):
        """Create initial mapping.

        Create initial mapping of all potential answers and acceptable
        guesses to a given state.
        """
        state_space = np.zeros((len(self.wordlist.answers),
                                len(self.wordlist.acceptable_guesses)),
                                dtype=int)

        for i, target in enumerate(self.wordlist.answers):
            for j, guess in enumerate(self.wordlist.acceptable_guesses):
                state_space[i, j] = helper.generate_state(target, guess)

        # Cache initial mapping on disk.
        np.save(STATE_PATH, state_space)
        return state_space

    def __init__(self, wordlist=wordle.WordList()):
        self.wordlist = wordlist

        if os.path.isfile(STATE_PATH):
            self.state_space = np.load(STATE_PATH)
        else:
            self.state_space = self.__create_state_space()

    def guess(self, game: wordle.WordleGame):
        """Determine optimal guess.
        """
        if game.round == 1:
            return self.first_guess

        answers = filter_answers(game)
        if len(answers) <= 2:
            return answers[0]
        elif len(answers) == 0:
            raise ValueError("No valid guesses left!")

        N, M = self.state_space.shape
        filter_mat = np.ones(N, dtype=int)
        for i, guess in enumerate(game.guesses):

            state = convert_state(game.state[i])
            guess_num = self.wordlist.word_index(guess)
            filter_mat[self.state_space[:, guess_num] != state] = 0

        counts = helper.calculate_counts(self.state_space, filter_mat)

        entropy = helper.calc_entropy(counts)

        guess_num = np.argmin(entropy)
        guess = self.wordlist.acceptable_guesses[guess_num]

        return guess
