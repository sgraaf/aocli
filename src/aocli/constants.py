import re
from datetime import datetime
from pathlib import Path

DEFAULT_DAY = datetime.now().day
DEFAULT_YEAR = datetime.now().year

YEAR_START = 2015
YEAR_END = DEFAULT_YEAR if datetime.now().month == 12 else DEFAULT_YEAR - 1
DAY_START = 1
DAY_END = 25

CONFIG_DIR = Path.home() / ".config" / "aocli"
if not CONFIG_DIR.is_dir():
    CONFIG_DIR.mkdir(parents=True)
SESSION_COOKIE_FILE = CONFIG_DIR / "session_cookie"

URL_TEMPLATE = "https://adventofcode.com/{year}/day/{day}"
URL_PATTERN = re.compile(r"https://adventofcode.com/(\d+)/day/(\d+)")

SOLUTION_TEMPLATE = """from aocli import read

print("{day_name}")

# read the input data from `input.txt`
data = read("input.txt")

# part one
print("--- Part One ---")

# part two
print("--- Part Two ---")
"""

CORRECT_STR_START = "That's the right answer"
CORRECT_STR_SUFFIX = " [Continue to Part Two]"
INCORRECT_STR_START = "That's not the right answer"
INCORRECT_STR_SUFFIX_TEMPLATE = " (You guessed {answer}.) [Return to Day {day}]"
WAIT_STR_START = "You gave an answer too recently"
WAIT_STR_SUFFIX_TEMPLATE = " [Return to Day {day}]"
