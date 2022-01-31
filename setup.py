from setuptools import setup
from Cython.Build import cythonize

setup(
    name='wordle-game',
    version='0.1',
    description='Play and solve Wordle games.',
    url='https://github.com/ahaque12/wordle-game',
    author='Adnan Haque',
    author_email='ahaque12@gmail.com',
    keywords='wordle game solver',
    project_urls={
        'Source': 'https://github.com/ahaque12/wordle-game',
        'Tracker': 'https://github.com/ahaque12/wordle-game/issues',

    },
    python_requires='>=3',
    data_files=[('data', ['data/wordle-allowed-guesses.txt',
                                  'data/wordle-answers-alphabetical.txt'])],
    entry_points={
        'console_scripts': [
            'wordle_game=wordle_game:main',
        ],
    },
    ext_modules=cythonize('helper.pyx')
)
