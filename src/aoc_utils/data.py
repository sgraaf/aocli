from typing import List


def to_lines(text: str) -> List[str]:
    """Split a string into (a list of) lines."""
    return text.splitlines()


def to_numbers(text: str) -> List[int]:
    """Split a string into a list of numbers."""
    return list(map(int, to_lines(text)))
