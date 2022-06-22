from pathlib import Path
from typing import Union

from .constants import SESSION_COOKIE_FILE


def read(file: Union[str, Path], encoding: str = "utf-8") -> str:
    """Read the contents of a file."""
    if not isinstance(file, Path):
        file = Path(file)

    if not file.exists():
        raise FileNotFoundError(f"File does not exist: {file}")

    with open(file, encoding=encoding) as fh:
        return fh.read()


def write(
    text: str,
    file: Union[str, Path],
    mode: str = "w",
    encoding: str = "utf-8",
    exist_ok: bool = True,
) -> None:
    """Write tect to a (plaintext) file."""
    if not isinstance(file, Path):
        file = Path(file)

    if file.exists() and not mode == "a" and not exist_ok:
        raise FileExistsError(
            f"File already exists: {file}. Use `exist_ok=True` to overwrite the existing file."
        )

    with open(file, mode, encoding=encoding) as fh:
        fh.write(text)


def get_session_cookie(
    session_cookie_file: Union[str, Path] = SESSION_COOKIE_FILE,
    raise_on_missing: bool = True,
) -> dict[str, str]:
    """Get the session cookie from the config directory."""
    if not isinstance(session_cookie_file, Path):
        session_cookie_file = Path(session_cookie_file)

    if not session_cookie_file.is_file():
        if raise_on_missing:
            raise ValueError(
                f"Session cookie does not exist: {session_cookie_file}. Please run `aocli init SESSION_COOKIE`."
            )
        return {}

    return {"session": read(session_cookie_file)}
