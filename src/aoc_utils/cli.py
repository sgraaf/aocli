from pathlib import Path

import typer
from lxml import html
from requests.exceptions import HTTPError

from .console import console
from .constants import (
    CONFIG_DIR,
    CORRECT_STR_START,
    CORRECT_STR_SUFFIX,
    DEFAULT_DAY,
    DEFAULT_YEAR,
    INCORRECT_STR_START,
    INCORRECT_STR_SUFFIX_TEMPLATE,
    SESSION_COOKIE_FILE,
    SOLUTION_TEMPLATE,
    URL_TEMPLATE,
    WAIT_STR_START,
    WAIT_STR_SUFFIX_TEMPLATE,
)
from .io import write
from .session import session


def raise_for_session_cookie():
    """Raise an exception if the session cookie is not set."""
    if session.cookies.get("session") is None:
        console.print(
            "Session cookie is not set. Please run `aocli init SESSION_COOKIE`."
        )
        raise typer.Exit(code=1)


app = typer.Typer(
    name="Advent of Code (AoC) CLI",
    no_args_is_help=True,
    help="Command-Line Interface (CLI) for Advent of Code (AoC). Supports fetching of input data and submission of answers.",
    short_help="CLI for Advent of Code (AoC)",
    add_completion=False,
)


@app.command()
def init(session_cookie: str) -> None:
    """Initialize the AoC session cookie."""
    # make config directory if it doesn't exist yet
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # write the session cookie to file in the config directory
    write(session_cookie, SESSION_COOKIE_FILE)
    console.print("Successfully initialized session cookie. ✨ 🍪 ✨")


@app.command()
def fetch(
    day: int = DEFAULT_DAY,
    year: int = DEFAULT_YEAR,
    force: bool = False,
    append_to_readme: bool = True,
) -> None:
    """Fetch the input (including test) data for the given day and create a barebones solution file."""
    raise_for_session_cookie()

    with console.status(f"Fetching input data for day {day} of year {year}..."):
        # get the url
        url = URL_TEMPLATE.format(day=day, year=year)
        try:
            r = session.get(url, raise_for_status=True)
        except ValueError as e:
            console.print(e)
            raise typer.Exit(code=1)
        except HTTPError as e:
            console.print(e)
            raise typer.Exit(code=1)

        # parse the html
        tree = html.fromstring(r.content)

        # get relevant data from the html
        day_name = tree.findtext(".//h2")
        test_inputs = [
            el.text
            for el in tree.iterfind(".//pre/code")
            if el.text == el.text_content()
        ]

        # make directory
        day_dir = Path(f"day{day:02d}")
        if day_dir.is_dir() and next(day_dir.iterdir(), None) is not None and not force:
            console.print(
                f"Directory {day_dir} already exists and is non-empty. Use `--force` to overwrite."
            )
            raise typer.Exit()
        day_dir.mkdir(exist_ok=True)

        # update README
        if append_to_readme:
            readme_file = Path("README.md")
            if not readme_file.is_file():
                console.print(
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
        try:
            r_data = session.get(url + "/input", raise_for_status=True)
        except ValueError as e:
            console.print(e)
            raise typer.Exit(code=1)
        except HTTPError as e:
            console.print(e)
            raise typer.Exit(code=1)
        write(r_data.text, day_dir / "input.txt")

        console.print("Done fetching. 📩")
        console.print(f"Go to part 1: {url}")


@app.command()
def submit(
    answer: str, part: int, day: int = DEFAULT_DAY, year: int = DEFAULT_YEAR
) -> None:
    """Submit an answer."""
    raise_for_session_cookie()

    with console.status(
        f"Submitting answer for part {part} of day {day} of year {year}..."
    ):
        # validate part
        if not 1 <= part <= 2:
            console.print(f"Invalid part: {part}. Must be either 1 or 2.")
            typer.Exit(code=1)

        try:
            r = session.post(
                url=URL_TEMPLATE.format(day=day, year=year) + "/answer",
                data={"level": str(part), "answer": answer},
                raise_for_status=True,
            )
        except ValueError as e:
            console.print(e)
            raise typer.Exit(code=1)
        except HTTPError as e:
            console.print(e)
            raise typer.Exit(code=1)

        # parse the html
        tree = html.fromstring(r.content)

        # get the feedback message
        msg = " ".join(tree.find(".//article/p").text_content().strip().split())

        if msg.startswith(CORRECT_STR_START):
            console.print(
                f'[bold green]Correct! 🌟:[/bold green] "{msg.removesuffix(CORRECT_STR_SUFFIX)}"'
            )
            if part == 1:
                console.print(
                    f"Continue to part 2: {URL_TEMPLATE.format(day=day, year=year)}#part2"
                )
        elif msg.startswith(INCORRECT_STR_START):
            console.print(
                f'[bold red]Incorrect! ❌:[/bold red] "{msg.removesuffix(INCORRECT_STR_SUFFIX_TEMPLATE.format(answer=answer, day=day))}"'
            )
        elif msg.startswith(WAIT_STR_START):
            console.print(
                f'[bold blue]Wait a minute! ⏱️:[/bold blue] "{msg.removesuffix(WAIT_STR_SUFFIX_TEMPLATE.format(day=day))}"'
            )


if __name__ == "__main__":
    app()
