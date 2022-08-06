import os

import numpy as np
from colorama import init, Fore

from solver import Figure

init(autoreset=True)

FILL_CHAR = "\u25FC"


def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_puzzle(
    puzzle: np.ndarray,
    figures: list[Figure],
    clear_screen: bool = True,
) -> None:
    if clear_screen:
        clear_terminal()

    figures_map = {figure.index: figure for figure in figures}

    for line in puzzle:
        line_str = ""
        for index, el in enumerate(line):
            match el:
                case -1:
                    ch = "{0}{1}".format(
                        Fore.RESET,
                        "·",
                    )
                case 0:
                    ch = "{0}{1}".format(
                        Fore.RESET,
                        " ",
                    )
                case _:
                    ch = "{0}{1}".format(
                        figures_map[el].color,
                        FILL_CHAR,
                    )

            line_str = "{0}{1}{2}{3}".format(
                line_str,
                "{0}|".format(Fore.BLACK),
                ch,
                "{0}|".format(Fore.BLACK) if index == len(line) - 1 else "",
            )

        print(line_str)
    print()
