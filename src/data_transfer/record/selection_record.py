from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from src.data_transfer.selection.bool_discrete_option import BoolDiscreteOption
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.option import Option

T = TypeVar("T")


class SelectionRecord(Generic[T]):
    """
    represents a selection containing the available options, the valid numbers of selected values and the selected
    values
    """

    def __init__(self, selected: List[T], option: Option[T], possible_selection_range: range = range(1, 2)):
        assert isinstance(selected, List)
        assert issubclass(option.__class__, Option)
        assert isinstance(possible_selection_range, range)

        self._option: Option[T] = option
        self._possible_selection_amount = possible_selection_range
        self._check_selected_valid(selected)
        self._selected: List[T] = selected

    @classmethod
    def bool(cls):
        """
        Create a bool selection
        """
        option = BoolDiscreteOption()
        return SelectionRecord([False], option)

    @classmethod
    def get_list_selection(cls, options: List[T], amount=range(1, 2)) -> Optional['SelectionRecord']:
        """
        creates a new selection record out of the given parameters
        :param options:    the options
        :param amount:     how many values can be selected
        :return            the new selection record
        """
        if len(options) <= 0:
            return None
        option_set: DiscreteOption = DiscreteOption(options)
        return SelectionRecord([options[0]], option_set, amount)

    @property
    def selected(self):
        """
        the selected value
        """
        return self._selected

    @property
    def option(self):
        """
        the options
        """
        return self._option

    @property
    def type(self) -> Optional[Type]:
        """
        the generic type
        """
        if len(self._selected) == 0:
            return None
        return type(self._selected[0])

    @property
    def possible_selection_amount(self):
        """
        the valid numbers of selected values
        """
        return self._possible_selection_amount

    def _check_selected_valid(self, selected: List[T]):
        if len(selected) not in self._possible_selection_amount:
            raise ValueError(f"{len(selected)} selections were made, but only "
                             f"{self._possible_selection_amount.start} up to {self._possible_selection_amount.stop - 1}"
                             f" option can be made.")
        for param in selected:
            if not self._option.is_valid(param):
                raise ValueError(f"The selected param {param} is not valid for option {self._option}.")

    def set_selected(self, selected: List[T]):
        """
        Sets the selected of the selection and returns the updated selection
        """
        self._check_selected_valid(selected)
        return SelectionRecord(selected, self._option, self._possible_selection_amount)

    def check_equal_type(self, selection) -> bool:
        """
        checks whether it is equal to the given selection record
        :param selection:   the other selection record
        :return             whether they are equal
        """
        if not isinstance(selection, SelectionRecord):
            return False
        if selection.type != self.type:
            if self.type == int or self.type == float:
                if not (selection.type == int or selection.type == float):
                    return False
            else:
                return False
        if selection.option != self.option:
            return False
        if selection.possible_selection_amount != self.possible_selection_amount:
            return False
        return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, SelectionRecord):
            return False
        if self._selected != other.selected:
            return False
        if self._possible_selection_amount != other._possible_selection_amount:
            return False
        if self._option != other.option:
            return False
        return True

    def __str__(self):
        return f"{self.__class__}\n" \
               f"\tselected: {self._selected}\n" \
               f"\tpossible amount: {self._possible_selection_amount}\n" \
               f"\toption: {self._option}"
