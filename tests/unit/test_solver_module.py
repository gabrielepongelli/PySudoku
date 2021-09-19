import pytest
from functools import wraps
from random import randrange


import sudoku.solver as sol


def init_cell_data(func):
    """Decorator that initialize some data for the tests of the class Cell."""
    wraps(func)

    def wrapper(self, *args, **kwargs):
        if self.args == None or self.cell == None:
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
