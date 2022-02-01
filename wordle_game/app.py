"""Streamlit app to play Wordle.

Inspired by https://github.com/sejaldua/wordle-analysis.
"""
import streamlit as st

import numpy as np
from wordle_game import wordle, solver

color_map = {2: 'green', 1: 'yellow', 0: 'grey'}
css = """
<style type='text/css'>
green {
    color: #ffffff;
    background-color: #6aaa64;
}
yellow {
    color: #ffffff;
    background-color: #c9b458;
}
grey {
    color: #ffffff;
    background-color: #787c7e;
}
white {
    background-color: #ffffff;
}
green, yellow, grey {
    border-style: solid;
    border-color: #ffffff;
    padding: 0.5em;
    text-align: center;
    font-weight: bold;
    font-size: 2rem;
    display: inline-block;
} 
</style>
""" 

solver_type = None
solve = None


def get_html(type, str_):
    return """<%(type)s>%(str)s</%(type)s>""" % {'type': type, 'str': str_ }


def state_repr(game):
    def map_int(x):
        if x == wordle.GREY:
            return 'grey'
        elif x == wordle.GREEN:
            return 'green'
        elif x == wordle.YELLOW:
            return 'yellow'

    output = ""
    _, M = game.state.shape
    N = len(game.guesses)
    for i in range(N):
        for j in range(M):
            output += get_html(map_int(game.state[i, j]), game.guesses[i][j].upper())
        output += "<br>"
    return output


def update_solver():
    global solve

    if solver_type == "Random":
        solve = solver.RandomSolver(game.wordlist)
    elif solver_type == "Max Entropy": 
        solve = solver.MaxEntropy(game.wordlist)

# -- Set page config
st.set_page_config(
   page_title="Wordle",
   page_icon=":thought_balloon:",
   layout="wide",
   initial_sidebar_state="expanded",
)

# Title the app
st.title('Wordle Game with Solver')

st.markdown("""
 * Play the wordle game below
 * You can use the solver on the left
""")

st.sidebar.markdown("## Select Solver")

button = st.sidebar.button('Reset game')
solver_type = st.sidebar.radio('How do you want to solve the Wordle?',
                               ['Random', 'Max Entropy'],
                               index=1,
                               on_change=update_solver
                               )
show_answers = st.sidebar.checkbox('Display words')

if 'game' not in st.session_state:
    game = wordle.WordleGame()
    update_solver()
    st.session_state['game'] = game
    st.session_state['solve'] = solve
else:
    game = st.session_state['game']
    solve = st.session_state['solve']

if button:
    wordlist = game.wordlist
    game = wordle.WordleGame(wordlist)
    st.session_state['game'] = game

with st.form("guess_form"):
    guess = st.text_input('Guess')
    # Every form must have a submit button.
    submitted = st.form_submit_button("ENTER")
    if submitted:
        if game.wordlist.valid_guess(guess):
            game.guess(guess)
            if game.complete() == wordle.WIN:
                st.info("You won!")
                st.balloons()
                del st.session_state['game']
            elif game.complete() == wordle.LOSE:
                st.info("You lost :(")
                del st.session_state['game']
        else:
            st.warning("Invalid guess!")


st.write(state_repr(game) + css, unsafe_allow_html=True)

st.sidebar.write("Best guess: " + solve.guess(game))
guess_list = solver.filter_answers(game)
st.sidebar.write("Number of acceptable answers remaining: " + str(len(guess_list)))
if show_answers:
    st.sidebar.write(guess_list)
