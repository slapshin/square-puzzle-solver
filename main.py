import json
import logging

import numpy as np
from blessed import Terminal
from colorama import ansi

import ui
from solver import Figure, PuzzleSolver

logging.basicConfig(
    # level=logging.INFO,
    level=logging.DEBUG,
    format="%(message)s",
)

COLORS = [
    getattr(ansi.Fore, name)
    for name in dir(ansi.Fore)
    if not name.startswith("_")
]

with open("puzzle.json") as file_ptr:
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

logging.info("# PUZZLE")
ui.print_array(puzzle)

logging.info("# FIGURES")
for figure in figures:
    logging.info("## figure №{0}".format(figure.index))
    logging.info("-" * 10)
    logging.info("### source shape")
    logging.info("-" * 5)
    ui.print_array(figure.source_shape, fore_color=figure.color)
    logging.info("### variants")
    for shape in figure.shapes:
        ui.print_array(shape, fore_color=figure.color)
        logging.info("-" * 5)
    logging.info("-" * 10)

# exit(1)

solver = PuzzleSolver(puzzle, figures)
solution = solver.solve()
if solution is not None:
    logging.info("solution found!!!")
    # ui.print_array(solution)
    ui.print_solution(solution, figures)
else:
    logging.info("solution is not found")
