"""Solve today's wordle in browser.

Selenium interaction inspired by https://github.com/Kubasinska/Wordle-Solver.
"""

import sys
import time
import re
import warnings

warnings.filterwarnings("ignore")

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from wordle_game import wordle, solver

WAIT_TIME = 1.5 # Wait between guesses.
START_TIME = 1 # Wait at start of loading.
END_TIME = 10 # Wait at the end of solving.


class Website:
    """Manage interactions with wordle website.
    """
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.powerlanguage.co.uk/wordle/')
        time.sleep(START_TIME)
        self.background = self.browser.find_element(By.TAG_NAME, 'html')
        self.background.click()
        time.sleep(START_TIME)
        self.round = 1

    def guess(self, word):
        self.background.send_keys(word)
        self.background.send_keys(Keys.ENTER)
        time.sleep(1)
        host = self.browser.find_element(By.TAG_NAME, "game-app")
        game = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('game')",
                                       host)
        board = game.find_element(By.ID, "board")
        rows = self.browser.execute_script("return arguments[0].getElementsByTagName('game-row')",
                                       board)
        row = self.browser.execute_script("return arguments[0].shadowRoot.querySelector("
                                      "'.row').innerHTML",
                                     rows[self.round - 1])
        self.round += 1

        bs_text = BeautifulSoup(row, 'html.parser')
        results = []
        for i, word in enumerate(bs_text.findAll('game-tile')):
            letter = word.get('letter')
            eval = word.get('evaluation')
            results.append(eval)

        return results


def main():
    web = Website()

    game = wordle.WordleGame()
    solve = solver.MaxEntropy(game.wordlist)

    for round in range(wordle.MAX_GUESSES):
        guess = solve.guess(game)
        response = web.guess(guess)

        state = ""
        for i, c in enumerate(guess):
            if response[i] == 'correct':
                state += 'G'
            elif response[i] == 'present':
                state += 'Y'
            else:
                state += 'B'

        game.add_state(guess, state)

        complete = game.complete()
        if complete == wordle.WIN:
            print("You won!")
            break
        elif complete == wordle.LOSE:
            print("You exceeded the maximum guesses and lost :(.")

        time.sleep(WAIT_TIME)
    time.sleep(END_TIME)


if __name__ == "__main__":
    main()
