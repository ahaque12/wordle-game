"""Module that implements command line tool.
"""

import argparse

import wordle
import solver


def play(args):
    game = wordle.WordleGame()

    while True:
        print("Game state:")
        print(game)
        guess = input("Enter guess:")
        guess = guess.lower().strip()
        if not game.wordlist.valid_guess(guess):
            print("Not a valid guess!")
            continue
        game.guess(guess)
        complete = game.complete()
        if complete == wordle.WIN:
            print("You won!")
            break
        elif complete == wordle.LOSE:
            print("You exceeded the maximum guesses and lost :(.")
            break


def assistant(args):
    """Assist Wordle gameplay.
    """
    game = wordle.WordleGame()
    if args.solver == 'random':
        solve = solver.RandomSolver(game.wordlist)
    elif args.solver == 'maxentropy':
        solve = solver.MaxEntropy(game.wordlist)

    while True:
        guess = input("Enter guess (enter empty string for no more guesses, list to see remaining valid answers):")
        if guess.strip() == "":
            print("Best guess is", guess)
            continue
        elif guess == "list":
            guess_list = solver.filter_answers(game)
            print("List of potential answers:")
            print(guess_list)
            continue

        response = input("Enter response:")
        while not wordle.valid_state(response):
            print("Enter a valid response.")
            response = input("Enter response:")
        game.add_state(guess, response)
        complete = game.complete()
        if complete == wordle.WIN:
            print("You won!")
            break
        elif complete == wordle.LOSE:
            print("You exceeded the maximum guesses and lost :(.")
            break


def main():
    parser = argparse.ArgumentParser("Play Wordle.")
    subparsers = parser.add_subparsers(help='Sub-command help.')

    parser_assistant = subparsers.add_parser('play', help='Play game')
    parser_assistant.set_defaults(func=play)

    parser_assistant = subparsers.add_parser('assistant', help='Use assistant')
    parser_assistant.add_argument('--solver', choices=['random', 'maxentropy'], default='random',
                                  help='Solver to use')
    parser_assistant.set_defaults(func=assistant)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()