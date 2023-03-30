from abc import ABC
from abc import abstractmethod
from typing import Optional

from src.controller.execution_handling.abstract_manager import AbstractManager
from src.controller.facade_consumer import FileFacadeConsumer
from src.controller.facade_consumer import SettingFacadeConsumer
from src.controller.output_handling.event import SettingsChanged
from src.data_transfer.content import type_check
from src.data_transfer.record import SettingsRecord


class ISettingManager(ABC):
    """This interface is responsible for controlled updating the settings in the model layer."""

    @abstractmethod
    def update_settings(self, settings_record: SettingsRecord) -> bool:
        """
        This method updates the model layer settings given a settings record

        :param settings_record: The settings record which includes all changes

        :return: whether the update was successful
        """

        pass

    @abstractmethod
    def import_settings(self, dict_name: str) -> bool:
        """
        imports the given settings
        """
        pass

    @abstractmethod
    def export_settings(self, dict_name: str) -> dict:
        """
        exports the current settings
        """
        pass


class ISettingGetter(ABC):
    """
    this interface encapsulates all getter-methods of a setting structure
    """

    @abstractmethod
    def get_settings_record(self) -> SettingsRecord:
        """
        This method gets the current settings

        :return: The current settings in a settings record
        """

        pass


class SettingManager(ISettingGetter, ISettingManager,
                     SettingFacadeConsumer, FileFacadeConsumer,
                     AbstractManager):
    """
    This class implements the setting model_manager interface. It uses the settingfacade of the model via the parental
    class to pass the changes through.
    """

    def __init__(self):
        ISettingGetter.__init__(self)
        ISettingManager.__init__(self)
        SettingFacadeConsumer.__init__(self)
        FileFacadeConsumer.__init__(self)
        AbstractManager.__init__(self)

    @type_check(SettingsRecord)
    def update_settings(self, settings_record: SettingsRecord) -> bool:

        if not self.setting_facade.update_settings(settings_record):
            self.handle_error([self._setting_facade])
            return False
        self.events.append(SettingsChanged())
        self.handle_event()
        return True

    @type_check(str)
    def import_settings(self, dict_name: str) -> bool:
        settings_dict = self.file_facade.import_dictionary_from_standard_path(dict_name)
        if settings_dict is None:
            self.handle_error([self._file_facade])
            return False

        if not self.setting_facade.load_from_dictionary(settings_dict):
            self.handle_error([self._setting_facade])
            return False

        return True

    @type_check(str)
    def export_settings(self, dict_name: str) -> Optional[dict]:

        dictionary = self.setting_facade.get_dictionary()
        if dictionary is None:
            self.handle_error([self._setting_facade])
            return None

        if not self.file_facade.export_dictionary_to_standard_path(dict_name, dictionary):
            self.handle_error([self._file_facade])
            return None

        return dictionary

    def get_settings_record(self) -> Optional[SettingsRecord]:
        settings: SettingsRecord = self.setting_facade.get_settings_record()
        if settings is None:
            self.handle_error([self._setting_facade])
            return None
        return settings
