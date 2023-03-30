from typing import List
from typing import Optional
from uuid import UUID

from src.controller.communication_facade import CommunicationFacade
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


class CommandInput(CommunicationFacade):
    """represents the Communication facade: receives user-input from the view"""

    def __init__(self):
        self._command_handler: Optional[ICommandManager] = None
        self._factory: Optional[ICommandFactory] = None
        self.appication_manager = None

    @logging
    def stop(self):
        """
        stops the application
        """
        pass

    @logging
    def set_command_handler(self, command_handler: ICommandManager):
        """
        sets the command handler
        :param command_handler: the command handler
        """
        self._command_handler = command_handler

    @logging
    def set_factory(self, factory: ICommandFactory):
        """
        sets the factory
        :param factory: the factory
        """
        self._factory = factory

    def set_application_manager(self, application_manager):
        """
        sets the application manager
        :param application_manager: the application manager
        """
        self.appication_manager = application_manager

    @logging
    def stop(self):
        """
        stops the application
        """
        self.appication_manager.stop()

    @logging
    def open_dataset(self, dataset_id: UUID):
        """
        opens the dataset with the given id
        :param dataset_id:  the id of the datset to open
        """
        open_dataset_command = self._factory.create_open_dataset_command(dataset_id)
        self._command_handler.process_command(open_dataset_command)

    @logging
    def import_dataset(self, paths: List[str], name: str, file_format: str):
        """
        imports the dataset of the given path
        :param paths:    the path of the dataset
        :param name:    the _name of the dataset
        :param file_format: the file format
        """
        import_dataset_command = self._factory.create_import_dataset_command(paths,
                                                                             name, file_format)
        self._command_handler.process_command(import_dataset_command)

    @logging
    def export_dataset(self, path: str):
        """
        exports the currently opened dataset
        :param path:    the path
        """
        export_dataset_command = self._factory.create_export_dataset_command(path, "csv")
        self._command_handler.process_command(export_dataset_command)

    @logging
    def delete_dataset(self, dataset_id: UUID):
        """
        deletes the dataset of the given id
        :param dataset_id:  the id of the dataset to delete
        """
        delete_dataset_command = self._factory.create_delete_dataset_command(dataset_id)
        self._command_handler.process_command(delete_dataset_command)

    @logging
    def change_settings(self, settings: SettingsRecord):
        """
        changes the settings
        :param settings:    the new settings
        """
        change_settings_command = self._factory.create_change_settings_command(settings)
        self._command_handler.process_command(change_settings_command)

    @logging
    def add_filter_group(self, filter_group: FilterGroupRecord, parent: UUID):
        """
        adds a new filter group
        :param filter_group:    the parameters of the new group
        :param parent:          the id of the filter group which the new group will be added
        """
        add_filter_group_command = self._factory.create_add_filter_group_command(filter_group, parent)
        self._command_handler.process_command(add_filter_group_command)

    @logging
    def add_filter(self, filter_record: FilterRecord, parent_id: UUID):
        """
        adds a new filter
        :param filter_record: the parameters of the new filter
        :param parent_id: the id of the filter group which the new filter will be added
        """
        add_filter_command = self._factory.create_add_filter_command(filter_record, parent_id)
        self._command_handler.process_command(add_filter_command)

    @logging
    def delete_filter(self, filter_id: UUID):
        """
        deletes the filter with the given id
        :param filter_id:  the id of the filter to delete
        """
        delete_filter_command = self._factory.create_delete_filter_command(filter_id)
        self._command_handler.process_command(delete_filter_command)

    @logging
    def delete_filter_group(self, group: UUID):
        """
        deletes the filter group with the given id
        :param group:   the id of the group to delete
        """
        delete_filter_group_command = self._factory.create_delete_filter_group_command(group)
        self._command_handler.process_command(delete_filter_group_command)

    @logging
    def move_filter_to_group(self, filter_id: UUID, new_group: UUID):
        """
        moves the filter to another group
        :param filter_id:      the id of the filter to move
        :param new_group:   the id of the group
        :return:
        """
        move_filter_to_group_command = self._factory.create_move_filter_to_groupcommand(filter_id, new_group)
        self._command_handler.process_command(move_filter_to_group_command)

    @logging
    def change_filter_group(self, group_id: UUID, filter_group: FilterGroupRecord):
        """
        changes the filter group with the given id
        :param group_id:    the id of the group to change
        :param filter_group:       the new parameters of the group
        """
        change_filter_group_command = self._factory.create_change_filter_group_command(
            group_id,
            filter_group)
        self._command_handler.process_command(change_filter_group_command)

    @logging
    def change_filter(self, filter_id: UUID, filter_record: FilterRecord):
        """
        changes the filter with the given id
        :param filter_record:    the id of the filter to change
        :param filter_id:       the new parameters of the filter
        """
        change_filter_command = self._factory.create_change_filter_command(filter_id, filter_record)
        self._command_handler.process_command(change_filter_command)

    # @logging
    def add_polygon(self, polygon: PolygonRecord) -> None:
        """
        adds a new polygon to the polygon structure
        :param polygon: the parameters of the new polygon
        """
        add_polygon_command = self._factory.create_add_polygon_command(polygon)
        self._command_handler.process_command(add_polygon_command)

    @logging
    def delete_polygon(self, polygon_id: UUID):
        """
        deletes the polygon with the given id
        :param polygon_id:  the id of the polygon to delete
        """
        delete_polygon_command = self._factory.create_delete_polygon_command(polygon_id)
        self._command_handler.process_command(delete_polygon_command)

    @logging
    def undo(self):
        """
        undoes the last executed (undoable) concrete_command
        """
        undo_command = self._factory.create_undo_command()
        self._command_handler.process_command(undo_command)

    @logging
    def redo(self):
        """
        redoes the last redone concrete_command
        """
        redo_command = self._factory.create_redo_command()
        self._command_handler.process_command(redo_command)

    @logging
    def add_analysis(self, analysis_type: AnalysisTypeRecord):
        """
        adds a new analysis to the analysis structure
        :param analysis_type:   the type of the new analysis
        """
        add_analysis_command = self._factory.create_add_analysis_command(analysis_type)
        self._command_handler.process_command(add_analysis_command)

    @logging
    def change_analysis(self, analysis_id: UUID, new_analysis_settings: AnalysisRecord):
        """
        changes the analysis with the given id
        :param analysis_id:             the id of the analysis to change
        :param new_analysis_settings:   the new parameters of the analysis
        """
        change_analysis_command = self._factory.create_change_analysis_command(analysis_id,
                                                                               new_analysis_settings)
        self._command_handler.process_command(change_analysis_command)

    @logging
    def delete_analysis(self, analysis_id: UUID):
        """
        deletes the analysis of the given id
        :param analysis_id:     the id of the analysis to delete
        """
        delete_analysis_command = self._factory.create_delete_analysis_command(analysis_id)
        self._command_handler.process_command(delete_analysis_command)

    @logging
    def import_analysis_type(self, path: str):
        """
        imports a new analysis type
        :param path:    the path of the new analysis type
        """
        import_analysis_command = self._factory.create_import_analysis_command(path)
        self._command_handler.process_command(import_analysis_command)

    @logging
    def refresh_analysis(self, analysis_id: UUID):
        """
        refreshes the analysis of the given id
        :param analysis_id:     the id of the analysis
        """
        refresh_analysis = self._factory.create_refresh_analysis_command(analysis_id)
        self._command_handler.process_command(refresh_analysis)

    @logging
    def export_file(self, file: FileRecord, path: str):
        """
        exports the given file
        :param file:    the file to export
        :param path:    the path for the export
        """
        export_file_command = self._factory.create_export_file_command(path, file)
        self._command_handler.process_command(export_file_command)
