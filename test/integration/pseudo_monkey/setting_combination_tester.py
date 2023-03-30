from typing import List

from src.data_transfer.record import SettingRecord

def possible_settings_combinations(settings: List[SettingRecord]):
    """
    A helper function to get all possible combinations of the settings. It yields all possible combinations.
    :param settings: the settings as a list of SettingRecord that should be tested for all possible combinations
    :return: the next combination of the settings as a list of SettingRecord
    """
    if len(settings) == 0:
        yield []

    elif len(settings) == 1:
        for setting in possible_setting_combination(settings[0]):
            yield [setting]
    else:
        for i, setting in enumerate(settings):
            for concrete_setting in possible_setting_combination(setting):
                yield settings[:i] + [concrete_setting] + settings[i + 1:]


def possible_setting_combination(setting: SettingRecord, max_combinations: int = 20):
    """
    A helper function to get all possible combinations of the setting. It yields all possible combinations.
    :param setting: the setting as a SettingRecord that should be tested for all possible combinations
    :param max_combinations: the maximum number of combinations that should be yielded
    :yield: the next combination of the setting as a SettingRecord
    """
    for i, option in enumerate(setting.selection.option.get_option()):
        if i > max_combinations:
            break
        yield SettingRecord(_context=setting.context,
                            _selection=setting.selection.set_selected([option]),
                            _identifier=setting.identifier)