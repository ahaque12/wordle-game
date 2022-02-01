import pytest
from wordle_game import wordle


@pytest.fixture
def wordlist():
    return wordle.WordList()


@pytest.fixture
def game(wordlist):
    return wordle.WordleGame(wordlist)


def test_word_index(wordlist):
    assert wordlist.word_index('rando') == -1, "'rando' is not a legitimate guess!"
    assert wordlist.word_index('soare') == 10364, "'soare' is in position 10364!"


def test_valid_guess(wordlist):
    assert wordlist.valid_guess('abcde') is False, "'abcde' is not a legitimate guess!"
    assert wordlist.valid_guess('raise') is True, "'raise' is an acceptable guess!"


def test_game_round(game):
    assert game.round == 1, "Initial round for game is 1!"
