
wordle-answers-alphabetical.txt : 
	wget wordle-answers-alphabetical.txt -P data/

wordle-allowed-guesses.txt : 
	wget wordle-allowed-guesses.txt -P data/

.PHONY: clean

clean : 
	rm data/*