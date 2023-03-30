from abc import ABC
from abc import abstractmethod
from uuid import UUID

from src.controller.execution_handling.analysis_manager import IAnalysisGetter
from src.controller.execution_handling.analysis_manager import IAnalysisManager
from src.controller.execution_handling.database_manager import IDatabaseManager
from src.controller.execution_handling.export_manager import IExportManager
from src.controller.execution_handling.filter_manager.filter_manager import IFilterGetter
from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.execution_handling.polygon_manager import IPolygonManager
from src.controller.execution_handling.setting_manager import ISettingGetter
from src.controller.execution_handling.setting_manager import ISettingManager
from src.controller.input_handling.commands.command_manager import ICommandManager
from src.controller.input_handling.commands.concrete_command.add_analysis import AddAnalysisCommand
from src.controller.input_handling.commands.concrete_command.add_filter import AddFilterCommand
from src.controller.input_handling.commands.concrete_command.add_filter_group import AddFilterGroupCommand
from src.controller.input_handling.commands.concrete_command.add_polygon import AddPolygonCommand
from src.controller.input_handling.commands.concrete_command.change_analysis import ChangeAnalysisCommand
from src.controller.input_handling.commands.concrete_command.change_filter import ChangeFilterCommand
from src.controller.input_handling.commands.concrete_command.change_filter_group import ChangeFilterGroupCommand
from src.controller.input_handling.commands.concrete_command.change_settings import ChangeSettingsCommand
from src.controller.input_handling.commands.concrete_command.delete_analysis import DeleteAnalysisCommand
from src.controller.input_handling.commands.concrete_command.delete_dataset import DeleteDatasetCommand
from src.controller.input_handling.commands.concrete_command.delete_filter import DeleteFilterCommand
from src.controller.input_handling.commands.concrete_command.delete_filter_group import DeleteFilterGroupCommand
from src.controller.input_handling.commands.concrete_command.delete_polygon import DeletePolygonCommand
from src.controller.input_handling.commands.concrete_command.export_dataset import ExportDatasetCommand
from src.controller.input_handling.commands.concrete_command.export_file import ExportFileCommand
from src.controller.input_handling.commands.concrete_command.import_analysis import ImportAnalysisCommand
from src.controller.input_handling.commands.concrete_command.import_dataset import ImportDatasetCommand
from src.controller.input_handling.commands.concrete_command.move_filter_to_group import MoveFilterToGroupCommand
from src.controller.input_handling.commands.concrete_command.open_dataset import OpenDatasetCommand
from src.controller.input_handling.commands.concrete_command.redo import RedoCommand
from src.controller.input_handling.commands.concrete_command.refresh_analysis import RefreshAnalysisCommand
from src.controller.input_handling.commands.concrete_command.undo import UndoCommand
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import SettingsRecord


class ICommandFactory(ABC):

    @abstractmethod
    def create_add_analysis_command(self, analysis_type: AnalysisTypeRecord):
        """
        creates a new AddAnalysisCommand
        :param analysis_type:   the analysis type
        :return:                the command
        """
        pass

    @abstractmethod
    def create_add_filter_command(self, new_filter: FilterRecord, parent: UUID):
        """
        creates a new AddFilterCommand
        :param new_filter:  the new filter
        :param parent:      the parent
        :return:            the command
        """
        pass

    @abstractmethod
    def create_add_filter_group_command(self, new_filter: FilterGroupRecord, parent: UUID):
        """
        creates a new AddFilterGroupCommand
        :param new_filter:  the new filter
        :param parent:      the parent
        :return:            the command
        """
        pass

    @abstractmethod
    def create_add_polygon_command(self, polygon: PolygonRecord):
        """
        creates a new AddPolygonCommand
        :param polygon:     the polygon
        :return:            the command
        """
        pass

    @abstractmethod
    def create_change_analysis_command(self, analysis_id: UUID, analysis_setting: AnalysisRecord):
        """
        creates a new ChangeAnalysisCommand
        :param analysis_id:         the id of the analysis
        :param analysis_setting:    the new analysis setting
        :return:                    the command
        """
        pass

    @abstractmethod
    def create_change_filter_command(self, filter_id: UUID, new_filter: FilterRecord):
        """
        creates a new ChangeFilterCommand
        :param filter_id:   the id of the filter
        :param new_filter:  the new filter
        :return:            the command
        """
        pass

    @abstractmethod
    def create_change_filter_group_command(self, group_id: UUID, new_group: FilterGroupRecord):
        """
        creates a new ChangeFilterGroupCommand
        :param group_id:    the id of the group
        :param new_group:   the new group
        :return:            the command
        """
        pass

    @abstractmethod
    def create_change_settings_command(self, settings: SettingsRecord):
        """
        creates a new ChangeSettingsCommand
        :param settings:    the new settings
        :return:            the command
        """
        pass

    @abstractmethod
    def create_delete_analysis_command(self, analysis_id: UUID):
        """
        creates a new DeleteAnalysisCommand
        :param analysis_id: the id of the analysis
        :return:            the command
        """
        pass

    @abstractmethod
    def create_delete_filter_command(self, filter_id: UUID):
        """
        creates a new DeleteFilterCommand
        :param filter_id:   the id of the filter
        :return:            the command
        """
        pass

    @abstractmethod
    def create_delete_dataset_command(self, dataset_id: UUID):
        """
        creates a new DeleteDatasetCommand
        :param dataset_id:  the id of the dataset
        :return:            the command
        """
        pass

    @abstractmethod
    def create_delete_filter_group_command(self, group_id: UUID):
        """
        creates a new DeleteFilterGroupCommand
        :param group_id:    the id of the group
        :return:            the command
        """
        pass

    @abstractmethod
    def create_delete_polygon_command(self, polygon_id: UUID):
        """
        creates a new DeletePolygonCommand
        :param polygon_id:  the id of the polygon
        :return:            the command
        """
        pass

    @abstractmethod
    def create_export_dataset_command(self, path: str, file_format: str):
        """
        creates a new ExportDatasetCommand
        :param path:        the path
        :param file_format: the file format
        :return:            the command
        """
        pass

    @abstractmethod
    def create_export_file_command(self, path: str, file: FileRecord):
        """
        creates a new ExportFileCommand
        :param path:    the path
        :param file:    the file
        :return:        the command
        """
        pass

    @abstractmethod
    def create_import_analysis_command(self, path: str):
        """
        creates a new ImportAnalysisCommand
        :param path:    the path
        :return:        the command
        """
        pass

    @abstractmethod
    def create_import_dataset_command(self, paths, name: str, file_format: str):
        """
        creates a new ImportDatasetCommand
        :param paths:       the paths
        :param name:        the name
        :param file_format: the file format
        :return:            the command
        """
        pass

    @abstractmethod
    def create_move_filter_to_groupcommand(self, filter_id: UUID, group_id: UUID):
        """
        creates a new MoveFilterToGroupCommand
        :param filter_id:   the id of the filter
        :param group_id:    the id of the group
        :return:            the command
        """
        pass

    @abstractmethod
    def create_open_dataset_command(self, dataset_id: UUID):
        """
        creates a new OpenDatasetCommand
        :param dataset_id:  the id of the dataset
        :return:            the command
        """
        pass

    @abstractmethod
    def create_redo_command(self):
        """
        creates a new RedoCommand
        :return:    the command
        """
        pass

    @abstractmethod
    def create_undo_command(self):
        """
        creates a new UndoCommand
        :return:    the command
        """
        pass

    @abstractmethod
    def create_refresh_analysis_command(self, analysis_id: UUID):
        """
        creates a new RefreshAnalysisCommand
        :param analysis_id: the id of the analysis
        :return:            the command
        """
        pass


class CommandFactory(ICommandFactory):

    def __init__(self, analysis_manager: IAnalysisManager, analysis_getter: IAnalysisGetter,
                 database_manager: IDatabaseManager,
                 filter_manager: IFilterManager, filter_getter: IFilterGetter, export_manager: IExportManager,
                 polygon_manager: IPolygonManager,
                 setting_manager: ISettingManager, setting_getter: ISettingGetter, command_manager: ICommandManager):
        self.analysis_manager = analysis_manager
        self.analysis_getter = analysis_getter
        self.database_manager = database_manager
        self.filter_manager = filter_manager
        self.filter_getter = filter_getter
        self.export_manager = export_manager
        self.polygon_manager = polygon_manager
        self.settings_manager = setting_manager
        self.settings_getter = setting_getter
        self.command_manager = command_manager

    def create_add_analysis_command(self, analysis_type: AnalysisTypeRecord):
        return AddAnalysisCommand(self.analysis_manager, analysis_type)

    def create_add_filter_command(self, new_filter: FilterRecord, parent: UUID):
        return AddFilterCommand(new_filter, parent, self.filter_manager)

    def create_add_filter_group_command(self, new_filter: FilterGroupRecord, parent: UUID):
        return AddFilterGroupCommand(new_filter, parent, self.filter_manager)

    def create_add_polygon_command(self, polygon: PolygonRecord):
        return AddPolygonCommand(polygon, self.polygon_manager)

    def create_change_analysis_command(self, analysis_id: UUID, analysis_setting: AnalysisRecord):
        return ChangeAnalysisCommand(self.analysis_manager, self.analysis_getter, analysis_id, analysis_setting)

    def create_change_filter_command(self, filter_id: UUID, new_filter: FilterRecord):
        return ChangeFilterCommand(filter_id, new_filter, self.filter_manager, self.filter_getter)

    def create_change_filter_group_command(self, group_id: UUID, new_group: FilterGroupRecord):
        return ChangeFilterGroupCommand(group_id, new_group, self.filter_manager, self.filter_getter)

    def create_change_settings_command(self, settings: SettingsRecord):
        return ChangeSettingsCommand(self.settings_manager, self.settings_getter, settings)

    def create_delete_analysis_command(self, analysis_id: UUID):
        return DeleteAnalysisCommand(self.analysis_manager, analysis_id)

    def create_delete_filter_command(self, filter_id: UUID):
        return DeleteFilterCommand(filter_id, self.filter_manager)

    def create_delete_dataset_command(self, dataset_id: UUID):
        return DeleteDatasetCommand(dataset_id, self.database_manager)

    def create_delete_filter_group_command(self, group_id: UUID):
        return DeleteFilterGroupCommand(group_id, self.filter_manager)

    def create_delete_polygon_command(self, polygon_id: UUID):
        return DeletePolygonCommand(polygon_id, self.polygon_manager)

    def create_export_dataset_command(self, path: str, file_format: str):
        return ExportDatasetCommand(self.export_manager, path, file_format)

    def create_export_file_command(self, path: str, file: FileRecord):
        return ExportFileCommand(self.export_manager, file, path)

    def create_import_analysis_command(self, path: str):
        return ImportAnalysisCommand(self.analysis_manager, path)

    def create_import_dataset_command(self, paths, name: str, file_format: str):
        return ImportDatasetCommand(self.database_manager, paths, name, file_format)

    def create_move_filter_to_groupcommand(self, filter_id: UUID, group_id: UUID):
        return MoveFilterToGroupCommand(filter_id, group_id, self.filter_manager)

    def create_open_dataset_command(self, dataset_id: UUID):
        return OpenDatasetCommand(dataset_id, self.database_manager)

    def create_redo_command(self):
        return RedoCommand(self.command_manager)

    def create_undo_command(self):
        return UndoCommand(self.command_manager)

    def create_refresh_analysis_command(self, analysis_id: UUID):
        return RefreshAnalysisCommand(self.analysis_manager, analysis_id)
