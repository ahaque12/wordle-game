# Wordle Game

## Getting Started

### Dictionary


1. Download the target word list at `https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/a9e55d7e0c08100ce62133a1fa0d9c4f0f542f2c/wordle-answers-alphabetical.txt` and place it in the `data/` folder.
1. Download the acceptable guesses word list at `https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/de1df631b45492e0974f7affe266ec36fed736eb/wordle-allowed-guesses.txt` and place it in the `data/` folder.

### Playing the game

There are two modes: assistant and play (WIP).

```bash
$ python3 main.py assistant random
Enter guess (enter empty string for no more guesses):raise
Enter response:BBBBG
Enter guess (enter empty string for no more guesses):belle
Enter response:BYYBG
Enter guess (enter empty string for no more guesses):clone
Enter response:BGBBG
Enter guess (enter empty string for no more guesses):
Best guess is elude
Enter response:YGGBG
Enter guess (enter empty string for no more guesses):fluke
Enter response:GGGBG
Enter guess (enter empty string for no more guesses):
Best guess is flume
Enter response:GGGBG
You exceeded the maximum guesses and lost :(.
```

### Solver assistant