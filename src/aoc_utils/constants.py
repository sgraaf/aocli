#!/usr/bin/env python
# coding: utf-8
from datetime import datetime
from pathlib import Path

from requests import Session

DEFAULT_DAY = datetime.now().day
DEFAULT_YEAR = datetime.now().year

CONFIG_DIR = Path.home() / ".config" / "aoc_utils"
if not CONFIG_DIR.is_dir():
    CONFIG_DIR.mkdir(parents=True)
SESSION_COOKIE_FILE = CONFIG_DIR / "session_cookie"

URL_TEMPLATE = "https://adventofcode.com/{year}/day/{day}"

SOLUTION_TEMPLATE = """#!/usr/bin/env python
# coding: utf-8
from aoc_utils import read

print("{day_name}")

# read the input data from `input.txt`
data = read("input.txt")

# part one
print("--- Part One ---")

# part two
print("--- Part Two ---")
"""

CORRECT_STR_START = "That's the right answer"
INCORRECT_STR_START = "That's not the right answer"
WAIT_STR_START = "You gave an answer too recently"

SESSION = Session()
SESSION.headers.update({"User-Agent": f"aoc_utils/0.1.0"})
