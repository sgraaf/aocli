def to_lines(text: str) -> list[str]:
    """Split a string into (a list of) lines."""
    return text.splitlines()


def to_numbers(text: str) -> list[int]:
    """Split a string into a list of numbers."""
    return list(map(int, to_lines(text)))
