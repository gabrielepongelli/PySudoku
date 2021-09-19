import pytest
from functools import wraps
from random import randrange


import sudoku.solver as sol


def init_cell_data(func):
    """Decorator that initialize some data for the tests of the class Cell."""
    wraps(func)

    def wrapper(self, *args, **kwargs):
        if (not hasattr(self, "args")) or (not hasattr(self, "cell")):
            self.args = {"value": 2, "row": 3, "col": 4}
            self.cell = sol.Cell(**self.args)
        return func(self, *args, **kwargs)

    return wrapper


class TestCellClass:
    """Test cases for the class Cell and its methods."""

    def test_init(self):
        """Test the init method of the class Cell."""

        args = {"value": 2, "row": 3, "col": 4}

        test = sol.Cell(**args)

        assert test.row == args["row"]
        assert test.col == args["col"]
        assert test._value == args["value"]

        with pytest.raises(sol.InvalidCellValueError):
            args = {"value": -1, "row": 3, "col": 4}
            test = sol.Cell(**args)

        with pytest.raises(sol.InvalidCellValueError):
            args = {"value": 10, "row": 3, "col": 4}
            test = sol.Cell(**args)

    @init_cell_data
    def test_value_getter(self):
        """Test the getter method for the value property of the class Cell."""

        assert self.cell.value == self.args["value"]

    @init_cell_data
    def test_value_setter(self):
        """Test the setter method for the value property of the class Cell."""

        self.cell.value = self.args["value"] + 1

        assert self.cell.value == self.args["value"] + 1

        with pytest.raises(sol.InvalidCellValueError):
            self.cell.value = -1

        with pytest.raises(sol.InvalidCellValueError):
            self.cell.value = 10

    @init_cell_data
    def test_eq(self):
        """Test the __eq__ method of the class Cell."""

        test = sol.Cell(self.args["value"], self.args["row"] + 1, self.args["col"])
        assert not (self.cell == test)

        test = sol.Cell(self.args["value"], self.args["row"], self.args["col"] + 1)
        assert not (self.cell == test)

        test = sol.Cell(self.args["value"] + 1, self.args["row"], self.args["col"])
        assert self.cell == test


def init_random_matrix():
    """Initialize a matrix 9x9 of random values in [0, 9]."""

    tmp_range = range(0, 9)

    matrix = []
    for _ in tmp_range:
        matrix.append([randrange(0, 10) for _ in tmp_range])

    return matrix


def init_board_data(func):
    """Decorator that initialize some data for the tests of the class Board."""

    wraps(func)

    def wrapper(self, *args, **kwargs):
        if (not hasattr(self, "matrix")) or (not hasattr(self, "board")):
            temp_matrix = init_random_matrix()
            self.matrix = []
            self.board = sol.Board()
            for i, row in enumerate(self.board._rows):
                self.matrix.append([])
                for j, cell in enumerate(row):
                    cell.value = temp_matrix[i][j]
                    self.matrix[i].append(sol.Cell(cell.value, cell.row, cell.col))

        return func(self, *args, **kwargs)

    return wrapper


class TestBoardClass:
    """Test cases for the class Board and its methods."""

    def test_init(self):
        """Test the init method of the class Board."""

        b = sol.Board()

        assert len(b._rows) == 9
        assert len(b._cols) == 9
        assert len(b._squares) == 9

        values = {c.value for col in b._rows for c in col}
        assert values == {0}

        values = {c.value for row in b._cols for c in row}
        assert values == {0}

        values = {c.value for square in b._squares for c in square}
        assert values == {0}

    def test_from_matrix(self):
        """Test the form_matrix class method of the class Board."""

        matrix = init_random_matrix()

        b = sol.Board.from_matrix(matrix)

        test = []
        for row in b._rows:
            test.append([c.value for c in row])

        assert matrix == test

    @init_board_data
    def test_get_cells(self):
        """Test the get_cells method of the class Board."""

        # test used cells
        test = [cell for row in self.matrix for cell in row if cell.value != 0]
        assert self.board.get_cells() == test

        # test not used cells
        test = [cell for row in self.matrix for cell in row if cell.value == 0]
        assert self.board.get_cells(used=False) == test

        # test row cells
        rows = 3
        test = [
            cell
            for row in self.matrix
            for cell in row
            if (cell.row == rows and cell.value != 0)
        ]
        assert self.board.get_cells(row=rows) == test

        # test col cells
        col = 3
        test = [
            cell
            for row in self.matrix
            for cell in row
            if (cell.col == col and cell.value != 0)
        ]
        assert self.board.get_cells(col=col) == test

        # test row and col cells
        rows = 4
        col = 3
        test = [
            cell
            for row in self.matrix
            for cell in row
            if (cell.col == col and cell.row == rows and cell.value != 0)
        ]
        assert self.board.get_cells(row=rows, col=col) == test

    @init_board_data
    def test_rows(self):
        """Test the rows method of the class Board."""

        assert self.board.rows() == self.matrix

    @init_board_data
    def test_cols(self):
        """Test the cols method of the class Board."""

        test = []
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if i == 0:
                    test.append([])
                test[j].append(cell)

        assert self.board.cols() == test

    @init_board_data
    def test_squares(self):
        """Test the squares method of the class Board."""

        test = []
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if j % 3 == 0 and i % 3 == 0:
                    test.append([])
                test[(j // 3) * ((i // 3) + 1)].append(cell)

        assert self.board.squares() == test

    @init_board_data
    def test_to_matrix(self):
        """Test the to_matrix method of the class Board."""

        test = []
        for row in self.matrix:
            test.append([cell.value for cell in row])

        assert self.board.to_matrix() == test
