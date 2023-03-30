from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.option_type import OptionType


class BoolDiscreteOption(DiscreteOption):
    """
    represents an option with a boolean value
    """

    def __init__(self):
        """
        Constructor for a boolean options et
        """
        super().__init__([True, False])
        self._optionType = OptionType.BOOL_OPTION
