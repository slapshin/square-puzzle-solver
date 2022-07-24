import logging

import numpy as np
from colorama import init, Fore

from solver import Figure

init(autoreset=True)

FILL_CHAR = "\u25FC"
EMPTY_CELL_CHAR = "\u00B7"


def print_array(
        ar: np.ndarray,
        fore_color: str | None = None,
        is_debug=False,
) -> None:
    for line in ar:
        line_str = ""
        for el in line:
            ch = str(el)
            line_str = "{0}{1}{2:>3s}".format(
                line_str,
                fore_color or "",
                ch,
            )
        if is_debug:
            logging.debug(line_str)
        else:
            logging.info(line_str)


def print_solution(ar: np.ndarray, figures: list[Figure]) -> None:
    figures_map = {figure.index: figure for figure in figures}
    for line in ar:
        line_str = ""
        for el in line:
            match el:
                case -1:
                    ch = "{0}{1}".format(
                        Fore.RESET,
                        EMPTY_CELL_CHAR,
                    )
                case _:
                    ch = "{0}{1}".format(
                        figures_map[el].color,
                        FILL_CHAR,
                    )
            line_str = "{0}{1}".format(line_str, ch)
        logging.info(line_str)
