"""Streamlit app to play Wordle.

Inspired by https://github.com/sejaldua/wordle-analysis.
"""
import streamlit as st

import numpy as np
import wordle

color_map = {2: 'green', 1: 'yellow', 0: 'grey'}
css = """
<style type='text/css'>
green {
    color: #00ff00;
}
yellow {
    color: #FFFF00;
}
grey {
    color: #808080;
}
white {
    color: #fff;
}
</style>
""" 


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
            output += get_html(map_int(game.state[i, j]), game.guesses[i][j])
        output += "<br>"
    return output

# -- Set page config
apptitle = 'Wordle'

# Title the app
st.title('Wordle Game with Solver')

st.markdown("""
 * Play the wordle game below
 * You can use the solver on the left
""")

if 'game' not in st.session_state:
    game = wordle.WordleGame()
    st.session_state['game'] = game
else:
    game = st.session_state['game']

st.sidebar.markdown("## Select Solver")

#-- Set time by GPS or event
select_event = st.sidebar.selectbox('How do you want to solve the Wordle?',
                                    ['Random'])

with st.form("guess_form"):
    guess = st.text_input('Guess')
    # Every form must have a submit button.
    submitted = st.form_submit_button("ENTER")
    game.guess(guess)

st.write(state_repr(game) + css, unsafe_allow_html=True)
