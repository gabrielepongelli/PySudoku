from typing import List
from .board import Board as _Board
from .generator import Generator as _Generator
from .generator import Difficulty as _Difficulty
from .solver import Solver as _Solver
from .utils import (
    InvalidDifficultyError,
    InvalidCellValueError,
    InvalidMatrixError,
    NoSolutionError,
)


class Sudoku:
    """Main class for creating and solving sudoku puzzles."""

    @staticmethod
    def generate(difficulty: str) -> List[List[int]]:
        """Generate a new sudoku puzzle with the specified difficulty.

        Args:
            difficulty (str): difficulty of the new puzzle. It can be easy,
            medium, hard or extreme.

        Returns:
            List[List[int]]: a matrix representing the new puzzle.

        Raises:
            InvalidDifficultyError if difficulty isn't one of the possible
            specified values.
        """

        try:
            difficulty = _Difficulty[difficulty.title()]
        except KeyError:
            raise InvalidDifficultyError(
                f"the difficulty level {difficulty} is not valid."
            )

        gen = _Generator(difficulty)
        return _Board.to_matrix(gen.generate().rows)

    @staticmethod
    def solve(matrix: List[List[int]]) -> List[List[int]]:
        """Solve the given sudoku puzzle.

        Args:
            matrix (List[List[int]]): matrix representing a sudoku puzzle.

        Returns:
            List[List[int]]: the matrix representing the solution to the given
            puzzle.

        Raises:
            InvalidMatrixError if the matrix passed is malformed or has no solution.
        """

        try:
            b = _Board.from_matrix(matrix)
            sol = _Solver.create(b)
            result = _Board.to_matrix(sol.solve().rows)
        except (InvalidCellValueError, NoSolutionError) as err:
            raise InvalidMatrixError(*err.args)

        return result