# exit.py

import sys
from src.ia import console

def error_exit(code: int = 1):
    """
    Exits the program with an error message and a non-zero exit code.
    """
    console.print("[red] Exiting...[/red]")
    sys.exit(code)
