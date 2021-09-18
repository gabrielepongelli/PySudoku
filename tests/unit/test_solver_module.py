from functools import wraps
import pytest
import sudoku.solver as sol


def init_cell_data(func):
    wraps(func)

    def wrapper(self, *args, **kwargs):
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
        """Test the setter method fot the value property of the class Cell."""

        self.cell.value = self.args["value"] + 1

        assert self.cell.value == self.args["value"] + 1

        with pytest.raises(sol.InvalidCellValueError):
            self.cell.value = -1

        with pytest.raises(sol.InvalidCellValueError):
            self.cell.value = 10
