
data : data/wordle-answers-alphabetical.txt data/wordle-allowed-guesses.txt
	ls data

data/wordle-answers-alphabetical.txt : 
	wget https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/a9e55d7e0c08100ce62133a1fa0d9c4f0f542f2c/wordle-answers-alphabetical.txt -P data/

data/wordle-allowed-guesses.txt : 
	wget https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/de1df631b45492e0974f7affe266ec36fed736eb/wordle-allowed-guesses.txt -P data/

.PHONY: clean

clean : 
	rm data/*