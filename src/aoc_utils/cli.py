#!/usr/bin/env python
# coding: utf-8
from pathlib import Path

import typer
from lxml import html

from .constants import (
    CONFIG_DIR,
    CORRECT_STR_START,
    DEFAULT_DAY,
    DEFAULT_YEAR,
    INCORRECT_STR_START,
    SESSION,
    SESSION_COOKIE_FILE,
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
    write(session_cookie, SESSION_COOKIE_FILE)
    SESSION.cookies.update({"session": session_cookie})
    typer.echo(f"Successfully initialized session cookie. ✨ 🍰 ✨")


@app.command()
def fetch(
    day: int = DEFAULT_DAY,
    year: int = DEFAULT_YEAR,
    force: bool = False,
    append_to_readme: bool = True,
) -> None:
    """Fetch the input (including test) data for the given day and create a barebones solution file."""
    # get the url
    url = URL_TEMPLATE.format(day=day, year=year)
    r = SESSION.get(url)
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
    if day_dir.is_dir() and next(day_dir.iterdir(), None) is not None and not force:
        typer.echo(
            f"Directory {day_dir} already exists and is non-empty. Use `--force` to overwrite."
        )
        raise typer.Exit()
    day_dir.mkdir(exist_ok=True)

    # update README
    if append_to_readme:
        readme_file = Path("README.md")
        if not readme_file.is_file():
            typer.echo(
                f"Could not find file {readme_file}. Use `--no-append_to_readme` to skip this step."
            )
            raise typer.Exit()
        write(
            f"* [{day_name.removeprefix('--- ').removesuffix(' ---')}](./{day_dir.name}) \n",
            readme_file,
            mode="a",
        )

    # create solution file
    write(SOLUTION_TEMPLATE.format(day_name=day_name), day_dir / "solution.py")

    # write test inputs to disk
    for i, test_input in enumerate(test_inputs):
        write(test_input, day_dir / f"test_{i:02d}.txt")

    # get the input data
    if SESSION.cookies.get("session") is None:
        SESSION.cookies.update(get_session_cookie())
    r_data = SESSION.get(url + "/input")
    r_data.raise_for_status()
    write(r_data.text, day_dir / "input.txt")

    typer.echo("Done fetching.")
    typer.echo(f"Go to part 1: {url}")


@app.command()
def submit(
    answer: str, part: int, day: int = DEFAULT_DAY, year: int = DEFAULT_YEAR
) -> None:
    """Submit an answer."""
    if SESSION.cookies.get("session") is None:
        SESSION.cookies.update(get_session_cookie())

    r = SESSION.post(
        url=URL_TEMPLATE.format(day=day, year=year) + "/answer",
        data={"level": str(part), "answer": answer},
    )
    r.raise_for_status()

    # parse the html
    tree = html.fromstring(r.content)

    # get the feedback message
    msg = tree.find(".//article/p").text_content()

    if msg.startswith(CORRECT_STR_START):
        typer.echo(msg.removesuffix(" [Continue to Part Two]"))
        if part == 1:
            typer.echo(f"Go to part 2: {URL_TEMPLATE.format(day=day, year=year)}#part2")
    elif msg.startswith(INCORRECT_STR_START):
        typer.echo(msg.removesuffix(f" (You guessed {answer}.) [Return to Day {day}]"))
    elif msg.startswith(WAIT_STR_START):
        typer.echo(msg)


if __name__ == "__main__":
    app()
