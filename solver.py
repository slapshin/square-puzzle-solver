import logging
from dataclasses import dataclass

import numpy as np

import ui

CELL_FREE = 0


@dataclass()
class Figure:
    color: str
    index: int
    source_shape: np.ndarray
    shapes: list[np.ndarray]


class PuzzleSolvedError(Exception):
    def __init__(self, solved_puzzle: np.ndarray):
        self._solved_puzzle = solved_puzzle

    def get_puzzle(self) -> np.ndarray:
        return self._solved_puzzle


class PuzzleSolver:
    def __init__(self, puzzle: np.ndarray, figures: list[Figure]):
        self._puzzle = puzzle
        self._figures = figures

    def solve(self) -> np.ndarray:
        try:
            self._start_iteration(
                1,
                self._puzzle,
                self._figures,
            )
        except PuzzleSolvedError as err:
            return err.get_puzzle()

    def _start_iteration(
            self,
            iteration_index: int,
            puzzle: np.ndarray,
            figures: list[Figure],
    ):
        logging.debug(
            "***** start iteration [{0}]. figures: {1} *****".format(
                iteration_index,
                ", ".join([str(figure.index) for figure in figures]),
            )
        )

        for index, figure in enumerate(figures):
            for shape_index, shape in enumerate(figure.shapes):
                logging.debug(
                    "*** place figure №{0}, shape #{1} ***".format(
                        figure.index,
                        shape_index,
                    )
                )

                logging.debug("input")
                ui.print_puzzle(puzzle, self._figures)
                logging.debug("-" * 5)

                new_puzzle = self._place_shape(figure, shape, puzzle)
                if new_puzzle is not None:
                    logging.debug("output")
                    ui.print_puzzle(new_puzzle, self._figures)

                    logging.debug("--- success ---")
                    new_figures = [
                        new_figure
                        for new_figure in figures
                        if new_figure != figure
                    ]

                    if not new_figures and self._puzzle_is_solved(new_puzzle):
                        raise PuzzleSolvedError(new_puzzle)

                    if new_figures:
                        self._start_iteration(
                            iteration_index + 1,
                            new_puzzle,
                            new_figures,
                        )
                else:
                    logging.debug("--- fail ---")

    def _place_shape(
            self,
            figure: Figure,
            shape: np.ndarray,
            puzzle: np.ndarray,
    ) -> np.ndarray | None:
        puzzle = puzzle.copy()

        puzzle_top_x, puzzle_left_y = self._get_puzzle_top_left(puzzle)

        shape_left = None

        for y in range(len(shape[0])):
            if shape[0, y] != CELL_FREE:
                shape_left = y
                break

        if shape_left is None:
            raise ValueError("can't detect shape start")
        for shape_x in range(len(shape)):
            for shape_y in range(len(shape[shape_x])):
                if shape[shape_x, shape_y] != CELL_FREE:
                    puzzle_x = puzzle_top_x + shape_x
                    puzzle_y = puzzle_left_y - shape_left + shape_y
                    if puzzle_y < 0:
                        return
                    try:
                        if puzzle[puzzle_x, puzzle_y] != CELL_FREE:
                            return
                    except IndexError:
                        return

                    puzzle[puzzle_x, puzzle_y] = figure.index

        return puzzle

    def _get_puzzle_top_left(
            self,
            puzzle: np.ndarray,
    ) -> tuple[int, int] | None:
        for x in range(puzzle.shape[0]):
            for y in range(puzzle.shape[1]):
                if puzzle[x, y] == CELL_FREE:
                    return x, y

    def _puzzle_is_solved(self, puzzle: np.ndarray) -> bool:
        for x in range(len(puzzle)):
            for y in range(len(puzzle[x])):
                if puzzle[x, y] == CELL_FREE:
                    return False

        return True
