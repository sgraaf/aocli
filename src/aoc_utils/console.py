from rich.console import Console
from rich.theme import Theme

console = Console(theme=Theme({"repr.str": "not bold not italic blue"}))
