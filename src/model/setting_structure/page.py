from typing import Dict
from typing import List

from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.settings_record import PageRecord
from src.model.setting_structure.segment import Segment


class Page:
    """
    A class to represent a Page containing Segments.
    """

    def __init__(self, identifier: SettingsEnum, name: str, segments: List[Segment]):
        """
        Initialize the Page with a _name and list of segments.

        :param name: The _name of the Page
        :type name: str
        :param segments: The list of Segment objects for the Page
        :type segments: List[Segment]
        """
        self._identifier: SettingsEnum = identifier
        self._name: str = name
        self._segments: List[Segment] = segments.copy()

    @classmethod
    def from_record(cls, record: PageRecord):
        """
        Create a Page instance from a PageRecord.

        :param record: The PageRecord to create the Page from
        :type record: PageRecord
        :return: A Page instance
        :rtype: Page
        """
        return cls(identifier=record.identifier, name=record.name,
                   segments=list(Segment.from_record(segment_record) for segment_record in record.segment_records))

    def create_segment(self, identifier: SettingsEnum, name: str) -> bool:
        """
        Creates a new segment within the page.

        :param identifier: The identifier for the new segment.
        :type identifier: str
        :param name: The name for the new segment.
        :type name: str
        :return: True if the segment was created successfully, False otherwise.
        :rtype: bool
        """
        for segment in self._segments:
            if segment.get_identifier() == identifier:
                return False
        self._segments.append(Segment(identifier, name, []))
        return True

    def create_setting(self, segment_identifier: SettingsEnum, identifier: SettingsEnum,
                       name: str, selection: SelectionRecord) -> bool:
        """
        Creates a new setting within the specified segment.

        :param segment_identifier: The identifier of the segment to add the setting to.
        :type segment_identifier: str
        :param identifier: The identifier for the new setting.
        :type identifier: str
        :param name: The name of the new setting.
        :type name: str
        :param selection: The record for the new setting.
        :type selection: SelectionRecord
        :return: True if the setting was created successfully, False otherwise.
        :rtype: bool
        """
        for segment in self._segments:
            if segment.get_identifier() == segment_identifier:
                return segment.create_setting(identifier=identifier, name=name, setting=selection)
        return False

    def get_identifier(self) -> SettingsEnum:
        """
        Gets the identifier for the page.

        :return: The identifier for the page.
        :rtype: str
        """
        return self._identifier

    def load_from_dict(self, dictionary: Dict) -> None:
        """
        Loads the contents of the page from a dictionary.

        :param dictionary: The dictionary containing the contents of the page.
        :type dictionary: dict
        """
        for segment in self._segments:
            segment.load_from_dict(dictionary)

    def export_to_dict(self, dictionary: Dict) -> Dict:
        """
        Exports the contents of the page to a dictionary.

        :param dictionary: The dictionary to export the contents to.
        :type dictionary: dict
        :return: The dictionary containing the contents of the page.
        :rtype: dict
        """
        for segment in self._segments:
            segment.export_to_dict(dictionary)
        return dictionary

    def get_record(self):
        """
        Creates an immutable snapshot of the current state of the page as a PageRecord.

        :return: The PageRecord mirroring the current state of the class
        :rtype: PageRecord
        """
        return PageRecord(_identifier=self._identifier,
                          _segments=tuple(segment.get_record() for segment in self._segments), _name=self._name)

    def get_name(self):
        """
        Get the _name of the Page.

        :return: The _name of the Page
        :rtype: str
        """
        return self._name

    def add_segment(self, segment: Segment) -> bool:
        """
        Add a Segment to the Page.

        :param segment: The Segment to add to the Page
        :type segment: Segment
        :return: Boolean indicating whether the Segment was added or not
        :rtype: bool
        """
        if segment in self._segments:
            return False
        self._segments.append(segment)
        return True

    def get_segments(self) -> List[Segment]:
        """
        Get the list of Segment objects for the Page.

        :return: A copy of the list of Segment objects for the Page
        :rtype: List[Segment]
        """
        return self._segments.copy()
