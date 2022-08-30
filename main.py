import json
import logging
import random
from argparse import ArgumentParser

import numpy as np
from colorama import ansi

import ui
from solver import Figure, PuzzleSolver

parser = ArgumentParser()
parser.add_argument(
    "-f",
    "--file",
    dest="filename",
    required=True,
    help="write report to FILE",
    metavar="FILE",
)

args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

COLORS = [
    getattr(ansi.Fore, name)
    for name in dir(ansi.Fore)
    if not name.startswith("_")
]
random.shuffle(COLORS)

with open(args.filename) as file_ptr:
    puzzle_data = json.load(file_ptr)

puzzle = np.array(puzzle_data["puzzle"])
puzzle[puzzle == 1] = -1

figures: list[Figure] = []

for figure_index, figure_data in enumerate(puzzle_data["figures"]):
    source_shape = np.array(figure_data)

    shapes = [source_shape]

    for index in range(0, 4):
        rotated = np.rot90(source_shape, index)

        if not any(np.array_equal(rotated, shape) for shape in shapes):
            shapes.append(rotated)

        flipped = np.flip(rotated, 1)
        if not any(np.array_equal(flipped, shape) for shape in shapes):
            shapes.append(flipped)

    figures.append(
        Figure(
            color=COLORS.pop(),
            source_shape=source_shape,
            shapes=shapes,
            index=figure_index + 1,
        )
    )

ui.print_puzzle(puzzle, figures)

solver = PuzzleSolver(puzzle, figures)
solution = solver.solve()
if solution is not None:
    ui.clear_terminal()
    ui.print_puzzle(solution.solved_puzzle, figures, clear_screen=False)
    print("iterations: {0}".format(solution.iterations))
else:
    print("solution is not found")
