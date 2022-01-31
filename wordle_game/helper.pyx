# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1

from wordle_game.wordle import GREEN, YELLOW, GREY, WORD_LEN
import numpy as np

# "cimport" is used to import special compile-time information
# about the numpy module (this is stored in a file numpy.pxd which is
# currently part of the Cython distribution).
cimport numpy as np

# It's necessary to call "import_array" if you use any part of the
# numpy PyArray_* API. From Cython 3, accessing attributes like
# ".shape" on a typed Numpy array use this API. Therefore we recommend
# always calling "import_array" whenever you "cimport numpy"
np.import_array()

# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.int

# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.int_t DTYPE_t


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
    cdef int state[5]
    cdef int i
    cdef char c

    # state=np.empty(WORD_LEN, dtype=int)
    for i in range(26):
        target_counter[i] = 0

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

    return state[0]+state[1]*3+state[2]*9+state[3]*27+state[4]*81


cpdef calculate_counts(np.ndarray state_space, np.ndarray filter_mat=None):

    cdef int i
    cdef int j
    cdef int answer_len = state_space.shape[0]
    cdef int guess_len = state_space.shape[1]

    if filter_mat is None:
        filter_mat = np.ones(answer_len, dtype=DTYPE)

    counts = np.zeros([guess_len, 3**5], dtype=DTYPE)

    for i in range(answer_len):
        if filter_mat[i] == 0:
            continue
        for j in range(guess_len):
            counts[j, state_space[i, j]] += 1

    return counts


cpdef calc_entropy(counts: np.ndarray):
    px = counts / (.001 + counts.sum(axis=1).reshape(-1, 1))
    entropy = np.sum(px*np.log2(px + .001), axis=1)
    return entropy


if __name__ == "__main__":
    for i in range(100000):
        generate_state("raise", "paire")