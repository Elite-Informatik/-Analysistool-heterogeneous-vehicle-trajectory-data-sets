from typing import List
from typing import Tuple
from uuid import UUID

from src.controller.input_handling.command_input import CommandInput
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.data_transfer.record import SettingsRecord


class ControllerCommunication:
    """
    This class is a proxy for the communication facade of the controller. It provides functionalities for
    the user interface elements, which allow them to perform commands on the controller and thus change
    and manipulate the data of the application.
    """

    def __init__(self, controller_communication: CommandInput):
        """
        Creates a new instance of the Controller Communication and sets the controller on which all commands should
        be executed. One instance is created on start of the User interface which is then used by all user interface
        elements. Thus all User Interface Elements perform their Operations on the same controller

        :param controller_communication: Interface of the Controller which provides concrete_command functionalities
        """
        self._controller_communication: CommandInput = controller_communication

    def open_dataset(self, uuid: UUID):
        """
        Tells the controller to open a dataset.

        :param uuid: id of the dataset
        """
        self._controller_communication.open_dataset(uuid)

    def export_dataset(self, path: str):
        """
        exports the currently opened dataset
        :param path:    the path
        """
        self._controller_communication.export_dataset(path)

    def import_dataset(self, path: List[str], name: str, file_format: str):
        """
        Tells the controller to import a new dataset.

        :param path: the path for the data of the dataset
        :param name: _name of the new dataset
        :param file_format: format of the dataset
        """
        self._controller_communication.import_dataset(path, name, file_format)

    def delete_polygon(self, uuid: UUID):
        """
        Tells the controller to delete a polygon.

        :param uuid: the id of the polygon that should be deleted
        """
        self._controller_communication.delete_polygon(uuid)

    def add_polygon(self, position_list: List[Tuple], name: str):
        """
        Tells the controller to create a new Polygon with the given _name based
        on the corner coordinates given as a list.

        :param position_list: list with the corner positions of the polygon
        :param name: _name of the polygon
        """
        corners = []
        for position in position_list:
            corners.append(PositionRecord(_latitude=position[0], _longitude=position[1]))
        polygon = PolygonRecord(_corners=tuple(corners), _name=name)
        self._controller_communication.add_polygon(polygon=polygon)

    def add_analysis(self, analysis_type: AnalysisTypeRecord):
        """
        adds a new analysis to the analysis structure
        :param analysis_type:   the type of the new analysis
        """
        self._controller_communication.add_analysis(analysis_type)

    def change_analysis(self, analysis_id: UUID, new_analysis_settings: AnalysisRecord):
        """
        changes the analysis with the given id
        :param analysis_id:             the id of the analysis to change
        :param new_analysis_settings:   the new parameters of the analysis
        """
        self._controller_communication.change_analysis(analysis_id, new_analysis_settings)

    def delete_analysis(self, analysis_id: UUID):
        """
        deletes the analysis of the given id
        :param analysis_id:     the id of the analysis to delete
        """
        self._controller_communication.delete_analysis(analysis_id)

    def import_analysis_type(self, path: str):
        """
        imports a new analysis type
        :param path:    the path of the new analysis type
        """
        self._controller_communication.import_analysis_type(path)

    def refresh_analysis(self, analysis_id: UUID):
        """
        refreshes the analysis of the given id
        :param analysis_id:     the id of the analysis
        """
        self._controller_communication.refresh_analysis(analysis_id)

    def export_file(self, file: FileRecord, path: str):
        """
        exports the given file
        :param file:    the file to export
        :param path:    the path for the export
        """
        self._controller_communication.export_file(file, path)

    def delete_dataset(self, dataset_id: UUID):
        """
        tells the controller to delete the dataset with the given id
        :param dataset_id: id of the dataset the user wants to delete
        """
        self._controller_communication.delete_dataset(dataset_id=dataset_id)

    def add_filter_group(self, filter_group_record: FilterGroupRecord, parent: UUID):
        """
        tells the controller to add the filter group to the filters.
        :param filter_group_record: the record that defines the filter group
        :param parent: the id of the parent filter group
        """
        self._controller_communication.add_filter_group(filter_group=filter_group_record, parent=parent)

    def add_filter(self, filter: FilterRecord, parent: UUID):
        """
        tells the controller to add the given filter as a child of the filter group with
        the given uuid.
        """
        self._controller_communication.add_filter(filter_record=filter, parent_id=parent)

    def change_filter(self, filter_id: UUID, filter_data: FilterRecord):
        """
        Tells the controller to change the data of the filter with the give id.
        """
        self._controller_communication.change_filter(filter_id=filter_id, filter_record=filter_data)

    def delete_filter(self, filter_component_id: UUID):
        """
        Tells the controller to delete the Filter with the corresponding uuid.
        """
        self._controller_communication.delete_filter(filter_id=filter_component_id)

    def change_filter_group(self, group_id: UUID, group_data: FilterGroupRecord):
        """
        Tells the controller to set the data of the filter group with the corresponding id
        to the values defined in the group_data record
        """
        self._controller_communication.change_filter_group(group_id=group_id, filter_group=group_data)

    def change_settings(self, settings: SettingsRecord):
        """
        Notifies the changes in the settings to the controller
        """
        self._controller_communication.change_settings(settings=settings)

    def close_application(self):
        """
        Tells the controller to close the application.
        """
        self._controller_communication.stop()

    def undo(self):
        """
        Tells the controller to undo the last operation
        """
        self._controller_communication.undo()

    def redo(self):
        """
        Tells the controller to redo the last operation
        """
        self._controller_communication.redo()
