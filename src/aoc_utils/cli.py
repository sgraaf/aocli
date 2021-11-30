#!/usr/bin/env python
# coding: utf-8
from pathlib import Path

import requests
import typer
from lxml import html

from .constants import (
    CONFIG_DIR,
    CORRECT_STR_START,
    DEFAULT_DAY,
    DEFAULT_YEAR,
    INCORRECT_STR_START,
    SOLUTION_TEMPLATE,
    URL_TEMPLATE,
    WAIT_STR_START,
)
from .io import get_session_cookie, write

app = typer.Typer()


@app.command()
def init(session_cookie: str) -> None:
    """Initialize the AoC session cookie."""
    if not CONFIG_DIR.is_dir():
        CONFIG_DIR.mkdir(parents=True)
    write(session_cookie, CONFIG_DIR / "session_cookie")


@app.command()
def fetch(day: int = DEFAULT_DAY, year: int = DEFAULT_YEAR):
    """Fetch the input (including test) data for the given day and create a barebones solution file."""
    # get the url
    r = requests.get(URL_TEMPLATE.format(day=day, year=year))
    r.raise_for_status()

    # parse the html
    tree = html.fromstring(r.content)

    # get relevant data from the html
    day_name = tree.findtext(".//h2")
    test_inputs = [
        el.text for el in tree.iterfind(".//pre/code") if el.text == el.text_content()
    ]

    # make directory
    day_dir = Path(f"day{day:02d}")
    day_dir.mkdir(exist_ok=True)

    # update README
    with open(Path("README.md"), "a", encoding="utf-8") as fh:
        fh.write(
            f"* [{day_name.removeprefix('--- ').removesuffix(' ---')}](./{day_dir.name})"
            + "\n"
        )

    # create solution file
    write(SOLUTION_TEMPLATE.format(day_name=day_name), day_dir / "solution.py")

    # write test inputs to disk
    for i, test_input in enumerate(test_inputs):
        write(test_input, day_dir / f"test_{i:02d}.txt")

    # get the input data
    r_data = requests.get(
        URL_TEMPLATE.format(day=day, year=year) + "/input", cookies=get_session_cookie()
    )
    r_data.raise_for_status()
    write(r_data.text, day_dir / "input.txt")


@app.command()
def submit(
    answer: str, part: int, day: int = DEFAULT_DAY, year: int = DEFAULT_YEAR
) -> None:
    """Submit an answer."""
    r = requests.post(
        url=URL_TEMPLATE.format(day=day, year=year) + "/answer",
        data={"level": str(part), "answer": answer},
        cookies=get_session_cookie(),
    )
    r.raise_for_status()

    # parse the html
    tree = html.fromstring(r.content)

    # get the feedback message
    msg = tree.find(".//article/p").text_content()

    if msg.startswith(CORRECT_STR_START):
        print("Correct!")
        print(msg)
        print(f"Go to part 2: {URL_TEMPLATE.format(day=day, year=year)}#part2")
    elif msg.startswith(INCORRECT_STR_START):
        print("Incorrect!")
        print(msg.removesuffix(f" (You guessed {answer}.) [Return to Day {day}]"))
    elif msg.startswith(WAIT_STR_START):
        print("You have to wait a bit longer before making another submission.")
        print(msg)


if __name__ == "__main__":
    app()
