from abc import ABC
from abc import abstractmethod
from typing import List
from uuid import UUID

from src.controller.input_handling.commands.command_factory import ICommandFactory
from src.controller.input_handling.commands.command_manager import ICommandManager
from src.data_transfer.content.logger import logging
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.data_transfer.record import SettingsRecord
from src.data_transfer.record.file_record import FileRecord
from src.data_transfer.record.filter_group_record import FilterGroupRecord
from src.data_transfer.record.filter_record import FilterRecord
from src.data_transfer.record.polygon_record import PolygonRecord


class CommunicationFacade(ABC):
    """represents the Communication facade: receives user-input from the view"""

    @logging
    @abstractmethod
    def stop(self):
        """
        stops the application
        """
        pass

    @logging
    @abstractmethod
    def set_command_handler(self, command_handler: ICommandManager):
        """
        sets the command handler
        :param command_handler: the command handler
        """
        pass

    @logging
    @abstractmethod
    def set_factory(self, factory: ICommandFactory):
        """
        sets the factory
        :param factory: the factory
        """
        pass

    @logging
    @abstractmethod
    def open_dataset(self, dataset_id: UUID):
        """
        opens the dataset with the given id
        :param dataset_id:  the id of the datset to open
        """
        pass

    @logging
    @abstractmethod
    def import_dataset(self, paths: List[str], name: str, file_format: str):
        """
        imports the dataset of the given path
        :param paths:    the path of the dataset
        :param name:    the _name of the dataset
        :param file_format: the file format
        """
        pass

    @logging
    @abstractmethod
    def export_dataset(self, path: str):
        """
        exports the currently opened dataset
        :param path:    the path
        """
        pass

    @logging
    @abstractmethod
    def delete_dataset(self, dataset_id: UUID):
        """
        deletes the dataset of the given id
        :param dataset_id:  the id of the dataset to delete
        """
        pass

    @logging
    @abstractmethod
    def change_settings(self, settings: SettingsRecord):
        """
        changes the settings
        :param settings:    the new settings
        """
        pass

    @logging
    @abstractmethod
    def add_filter_group(self, filter_group: FilterGroupRecord, parent: UUID):
        """
        adds a new filter group
        :param filter_group:    the parameters of the new group
        :param parent:          the id of the filter group which the new group will be added
        """
        pass

    @logging
    @abstractmethod
    def add_filter(self, filter_record: FilterRecord, parent_id: UUID):
        """
        adds a new filter
        :param filter_record: the parameters of the new filter
        :param parent_id: the id of the filter group which the new filter will be added
        """
        pass

    @logging
    @abstractmethod
    def delete_filter(self, filter_id: UUID):
        """
        deletes the filter with the given id
        :param filter_id:  the id of the filter to delete
        """
        pass

    @logging
    @abstractmethod
    def delete_filter_group(self, group: UUID):
        """
        deletes the filter group with the given id
        :param group:   the id of the group to delete
        """
        pass

    @logging
    @abstractmethod
    def move_filter_to_group(self, filter_id: UUID, new_group: UUID):
        """
        moves the filter to another group
        :param filter_id:      the id of the filter to move
        :param new_group:   the id of the group
        :return:
        """
        pass

    @logging
    @abstractmethod
    def change_filter_group(self, group_id: UUID, filter_group: FilterGroupRecord):
        """
        changes the filter group with the given id
        :param group_id:    the id of the group to change
        :param filter_group:       the new parameters of the group
        """
        pass

    @logging
    @abstractmethod
    def change_filter(self, filter_id: UUID, filter_record: FilterRecord):
        """
        changes the filter with the given id
        :param filter_record:    the id of the filter to change
        :param filter_id:       the new parameters of the filter
        """
        pass

    @logging
    @abstractmethod
    def add_polygon(self, polygon: PolygonRecord) -> None:
        """
        adds a new polygon to the polygon structure
        :param polygon: the parameters of the new polygon
        """
        pass

    @logging
    @abstractmethod
    def delete_polygon(self, polygon_id: UUID):
        """
        deletes the polygon with the given id
        :param polygon_id:  the id of the polygon to delete
        """
        pass

    @logging
    @abstractmethod
    def undo(self):
        """
        undoes the last executed (undoable) concrete_command
        """
        pass

    @logging
    @abstractmethod
    def redo(self):
        """
        redoes the last redone concrete_command
        """
        pass

    @logging
    @abstractmethod
    def add_analysis(self, analysis_type: AnalysisTypeRecord):
        """
        adds a new analysis to the analysis structure
        :param analysis_type:   the type of the new analysis
        """
        pass

    @logging
    @abstractmethod
    def change_analysis(self, analysis_id: UUID, new_analysis_settings: AnalysisRecord):
        """
        changes the analysis with the given id
        :param analysis_id:             the id of the analysis to change
        :param new_analysis_settings:   the new parameters of the analysis
        """
        pass

    @logging
    @abstractmethod
    def delete_analysis(self, analysis_id: UUID):
        """
        deletes the analysis of the given id
        :param analysis_id:     the id of the analysis to delete
        """
        pass

    @logging
    @abstractmethod
    def import_analysis_type(self, path: str):
        """
        imports a new analysis type
        :param path:    the path of the new analysis type
        """
        pass

    @logging
    @abstractmethod
    def refresh_analysis(self, analysis_id: UUID):
        """
        refreshes the analysis of the given id
        :param analysis_id:     the id of the analysis
        """
        pass

    @logging
    @abstractmethod
    def export_file(self, file: FileRecord, path: str):
        """
        exports the given file
        :param file:    the file to export
        :param path:    the path for the export
        """
        pass
