from wordle import GREEN, YELLOW, GREY, WORD_LEN
import numpy as np

cdef map_char(char x):
    return x - 97

cpdef generate_state(str target, str word):
    """Generate state of guess.

    Examples
    --------
    >>> np.all(generate_state("raise", "paire") == np.array([GREY, GREEN, GREEN, YELLOW, GREEN]))
    True
    >>> np.all(generate_state("boils", "loops") == np.array([YELLOW, GREEN, GREY, GREY, GREEN]))
    True
    >>> np.all(generate_state("flute", "belle") == np.array([GREY, GREY, YELLOW, GREY, GREEN]))
    True
    """
    cdef int target_counter[26]
    cdef int i
    cdef char c

    state = np.empty(WORD_LEN, dtype=int)
    for i in range(WORD_LEN):
        target_counter[map_char(ord(target[i]))] += 1
        if word[i] == target[i]:
            state[i] = GREEN
            target_counter[map_char(ord(word[i]))] -= 1

    for i in range(WORD_LEN):
        c = ord(word[i])
        if c == ord(target[i]):
            continue
        elif target_counter[map_char(c)] > 0:
            state[i] = YELLOW
        else:
            state[i] = GREY
            continue
        target_counter[map_char(c)] -= 1
    return state
