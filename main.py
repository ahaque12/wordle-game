"""Module that implements command line tool.
"""

import argparse

import wordle
import solver


def assistant(args):
    """Assist Wordle gameplay.
    """
    game = wordle.WordleGame()
    if args.solver == 'random':
        solve = solver.RandomSolver()

    while True:
        guess = input("Enter guess (enter empty string for no more guesses):")
        if guess.strip() == "":
            guess = solve.guess(game)
            print("Best guess is", guess)

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

    parser_assistant = subparsers.add_parser('assistant', help='Use assistant')
    parser_assistant.add_argument('solver', choices=['random'], help='Solver to use')
    parser_assistant.set_defaults(func=assistant)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()