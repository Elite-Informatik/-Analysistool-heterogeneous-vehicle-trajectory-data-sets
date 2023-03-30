from abc import ABC
from abc import abstractmethod

from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.settings_record import SettingsRecord


class ISettingStructure(ABC):
    """
    The class responsible for managing the settings of the application.
    It stores a list of Pages, which consist of Segments, which in turn consist of Settings.
    """

    @abstractmethod
    def add_page(self, name: str, identifier: str) -> bool:
        """
        Adds a new page object to the collection.

        :param name: The name of the new page.
        :type name: str
        :param identifier: The identifier for the new page.
        :type identifier: str
        :return: True if the page was added successfully, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def add_segment(self, name: str, identifier: str, page_identifier: str) -> bool:
        """
        Adds a new segment object to the specified page.

        :param name: The name of the new segment.
        :type name: str
        :param identifier: The identifier for the new segment.
        :type identifier: str
        :param page_identifier: The identifier for the page to add the segment to.
        :type page_identifier: str
        :return: True if the segment was added successfully, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def add_settings(self, page_identifier: str, segment_identifier: str, identifier: str, name: str,
                     selection: SelectionRecord) -> bool:
        """
        Adds a new setting to the specified segment.

        :param page_identifier: The identifier of the page that the segment belongs to.
        :type page_identifier: str
        :param segment_identifier: The identifier of the segment to add the setting to.
        :type segment_identifier: str
        :param identifier: The identifier for the new setting.
        :type identifier: str
        :param name: The name of the new setting.
        :type name: str
        :param selection: The record for the new setting.
        :type selection: SelectionRecord
        :return: True if the setting was added successfully, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_dictionary(self) -> dict:
        """
        Gets the collection of pages, segments and settings as a dictionary.

        :return: The collection as a dictionary.
        :rtype: dict
        """
        pass

    @abstractmethod
    def load_from_dictionary(self, setting_dictionary: dict) -> bool:
        """
        Loads the collection of pages, segments and settings from a dictionary.

        :param setting_dictionary: The dictionary containing the collection.
        :type setting_dictionary: dict
        :return: True if the collection was loaded successfully, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_settings_record(self) -> SettingsRecord:
        """
        Convert a list of Pages to a SettingsRecord instance.
        :return:
        """
        pass

    @abstractmethod
    def update_settings(self, settings: SettingsRecord) -> bool:
        """
        This method takes in a SettingsRecord and updates the SettingStructure's _pages attribute with the pages in the
        SettingsRecord.

        :param settings:
            The SettingsRecord to be used to update the SettingStructure's _pages attribute.

        :return:
            bool: True if the operation is successful.

        """
        pass
