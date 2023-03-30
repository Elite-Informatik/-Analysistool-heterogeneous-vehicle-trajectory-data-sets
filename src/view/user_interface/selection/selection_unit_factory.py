from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.option_type import OptionType
from src.view.user_interface.selection.selection_unit import SelectionUnit
from src.view.user_interface.selection.selection_unit_bool import BoolSelectionUnit
from src.view.user_interface.selection.selection_unit_date_interval import DateIntervalSelectionUnit
from src.view.user_interface.selection.selection_unit_discrete import DiscreteSelectionUnit
from src.view.user_interface.selection.selection_unit_interval_value import IntervalValueSelectionUnit
from src.view.user_interface.selection.selection_unit_number_interval import NumberIntervalSelectionUnit
from src.view.user_interface.selection.selection_unit_string import StringSelectionUnit
from src.view.user_interface.selection.selection_unit_time_interval import TimeIntervalSelectionUnit


class SelectionUnitFactory:
    """
    represents a factory to create selection unit
    """

    @staticmethod
    def create_selection_unit(setting_record: SettingRecord) -> SelectionUnit:
        """
        creates a selection unit out of the setting record
        :param setting_record:  the setting record
        :return:                the selection unit
        """
        setting_type = setting_record.selection.option.get_option_type()
        if setting_type == OptionType.STRING_OPTION:
            return StringSelectionUnit(setting_record)
        elif setting_type == OptionType.INTERVAL_OPTION:
            return IntervalValueSelectionUnit(setting_record)
        elif setting_type == OptionType.DISCRETE_OPTION:
            return DiscreteSelectionUnit(setting_record)
        elif setting_type == OptionType.BOOL_OPTION:
            return BoolSelectionUnit(setting_record)
        elif setting_type == OptionType.DATE_INTERVAL_OPTION:
            return DateIntervalSelectionUnit(setting_record)
        elif setting_type == OptionType.TIME_INTERVAL_OPTION:
            return TimeIntervalSelectionUnit(setting_record)
        elif setting_type == OptionType.NUMBER_INTERVAL_OPTION:
            return NumberIntervalSelectionUnit(setting_record)
