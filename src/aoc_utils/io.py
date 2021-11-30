#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
from typing import Dict

from .constants import CONFIG_DIR


def read(file: Path, encoding: str = "utf-8") -> str:
    """Read the contents of a file."""
    if not file.exists():
        raise FileNotFoundError(f"File does not exist: {file}")

    with open(file, "r", encoding=encoding) as fh:
        return fh.read()


def write(
    text: str, file: Path, encoding: str = "utf-8", exist_ok: bool = True
) -> None:
    """Write tect to a (plaintext) file."""
    if file.exists() and not exist_ok:
        raise FileExistsError(
            f"File already exists: {file}. Use `exist_ok=True` to overwrite the existing file."
        )

    with open(file, "w", encoding=encoding) as fh:
        fh.write(text)


def get_session_cookie() -> Dict[str, str]:
    """Get the session cookie from the config directory."""
    config_file = CONFIG_DIR / "session_cookie"
    if not config_file.is_file():
        raise ValueError(
            f"Session cookie does not exist: {config_file}. Please run `aocli init SESSION_COOKIE`."
        )

    return {"session": read(config_file)}
