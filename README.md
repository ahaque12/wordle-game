# Wordle Game

**Documentation:** https://ahaque12.github.io/wordle-game

### 😂 Here is a random joke that'll make you laugh!
![Jokes Card](https://readme-jokes.vercel.app/api)

## Getting Started

### Dictionary

Run the makefile `$ make` or download the dictionaries manually.

1. Download the target word list at `https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/a9e55d7e0c08100ce62133a1fa0d9c4f0f542f2c/wordle-answers-alphabetical.txt` and place it in the `data/` folder.
1. Download the acceptable guesses word list at `https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/de1df631b45492e0974f7affe266ec36fed736eb/wordle-allowed-guesses.txt` and place it in the `data/` folder.

You can install the package using:
```bash
$ python setup.py install
```
or 
```bash
$ pip install -e .
```

## Playing the game

### CLI
There are two modes: assistant and play.

#### Assistant
```bash
$ wordle_game assistant --solver random
Enter guess (enter empty string for no more guesses):raise
Enter response:BBBBG
Enter guess (enter empty string for no more guesses):belle
Enter response:BYYBG
Enter guess (enter empty string for no more guesses):clone
Enter response:BGBBG
Enter guess (enter empty string for no more guesses):
Best guess is elude
Enter guess (enter empty string for no more guesses):
Enter response:YGGBG
Enter guess (enter empty string for no more guesses):fluke
Enter response:GGGBG
Enter guess (enter empty string for no more guesses):
Best guess is flume
Enter guess (enter empty string for no more guesses):
Enter response:GGGBG
You exceeded the maximum guesses and lost :(.
```

#### Play
```bash
$ wordle_game assistant play
python3 main.py play
Game state:

Enter guess:raise
Game state:
YBBBB

Enter guess:spout
Game state:
YBBBB
BBYBB

```

### Streamlit

```bash
$ wordle_app streamlit
```
![image](https://user-images.githubusercontent.com/6743515/151911458-4225efcd-cfd0-4044-bd58-352249fd4b96.png)

