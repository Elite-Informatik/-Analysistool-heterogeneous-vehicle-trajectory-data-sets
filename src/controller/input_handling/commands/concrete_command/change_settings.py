from src.controller.execution_handling.setting_manager import ISettingGetter
from src.controller.execution_handling.setting_manager import ISettingManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import SettingsRecord


class ChangeSettingsCommand(Undoable):
    """
    represents a command to change the settings
    """

    def __init__(self, setting_manager: ISettingManager, setting_getter: ISettingGetter, settings: SettingsRecord):
        """
        creates a new ChangeSettingsCommand
        :param setting_manager: the settings manager
        :param settings:        the new settings
        """
        super().__init__()
        self._setting_manager = setting_manager
        self._setting_getter = setting_getter
        self._new_settings = settings
        self._old_settings = self._setting_getter.get_settings_record()

    def undo(self):
        """
        undoes itself: restores the old settings
        """
        self._setting_manager.update_settings(self._old_settings)

    def execute(self):
        """
        updates the settings
        """
        self._was_successful = self._setting_manager.update_settings(self._new_settings)
