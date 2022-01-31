from setuptools import setup
from Cython.Build import cythonize

import numpy as np

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='wordle-game',
    version='0.1',
    description='Play and solve Wordle games.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ahaque12/wordle-game',
    author='Adnan Haque',
    author_email='ahaque12@gmail.com',
    keywords='wordle game solver',
    project_urls={
        'Source': 'https://github.com/ahaque12/wordle-game',
        'Tracker': 'https://github.com/ahaque12/wordle-game/issues',

    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    packages=['wordle_game'],
    package_dir={'wordle_game': 'wordle_game'},
    data_files=[('data', ['wordle_game/data/wordle-allowed-guesses.txt',
                          'wordle_game/data/wordle-answers-alphabetical.txt'])],
    entry_points={
        'console_scripts': [
            'wordle_game=wordle_game.main:main',
            'wordle_app=wordle_game.app_wrapper:main',
        ],
    },
    ext_modules=cythonize('wordle_game/helper.pyx'),
    include_dirs=[np.get_include()],
)
