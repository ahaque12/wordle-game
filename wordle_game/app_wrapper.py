import click
import streamlit.cli
import os
from pathlib import Path


@click.group()
def main():
    pass


@main.command('streamlit')
def main_streamlit():
    filename = os.path.join(Path(__file__).parent, 'app.py')
    args = []
    streamlit.cli._main_run(filename, args)


if __name__ == "__main__":
    main()
