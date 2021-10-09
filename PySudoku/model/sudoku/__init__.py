from typing import List
from .board import Board as _Board
from .generator import Generator as _Generator
from .generator import Difficulty as _Difficulty
from .workers import Worker as _Worker
from .workers import WorkerType as _WorkerType
from .utils import InvalidDifficultyError


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

        b = _Board.from_matrix(matrix)
        sol = _Worker.create(_WorkerType.Solver, b)
        result = _Board.to_matrix(sol.resolve().rows)

        return result
