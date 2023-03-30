from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import List
from typing import Optional
from uuid import UUID

from src.controller.execution_handling.abstract_manager import AbstractManager
from src.controller.facade_consumer import AnalysisFacadeConsumer
from src.controller.facade_consumer import FileFacadeConsumer
from src.controller.output_handling.event import AnalysisAdded
from src.controller.output_handling.event import AnalysisChanged
from src.controller.output_handling.event import AnalysisDeleted
from src.controller.output_handling.event import AnalysisImported
from src.controller.output_handling.event import AnalysisRefreshed
from src.data_transfer.content import type_check
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord


class IAnalysisManager(ABC):
    """
    this interface represents an analysis manager
    """

    @abstractmethod
    def update_imported_analyses(self):
        """
        Updates the imported analyses
        """
        pass

    @abstractmethod
    def edit_analysis_settings(self, uuid: UUID, analysis_record: AnalysisRecord) -> bool:
        """
        Edits the settings of an analysis

        :param uuid: The uuid of the analysis to edit
        :param analysis_record: The new settings of the analysis

        :return: whether the edit was successful
        """

        pass

    @abstractmethod
    def add_analysis(self, analysis_type: AnalysisTypeRecord) -> bool:
        """
        Adds Analysis to the model layer

        :param analysis_type: The type of the analysis to add
        :return: whether the addition was successful
        """

        pass

    @abstractmethod
    def delete_analysis(self, uuid: UUID) -> bool:
        """
        Deletes an analysis from the model layer

        :param uuid: The uuid of the analysis to delete

        :return: whether the deletion was successful
        """

        pass

    @abstractmethod
    def refresh_analysis(self, uuid: UUID) -> bool:
        """
        Refreshes an analysis in the model layer

        :param uuid: The uuid of the analysis to refresh

        :return: whether the refresh was successful
        """

        pass

    @abstractmethod
    def import_analysis(self, path) -> bool:
        """
        Imports a script analysis in the program structure

        :param path: The path of the analysis to import

        :return: whether the import was successful
        """

        pass


class IAnalysisGetter(ABC):
    """
    this interface encapsulates the getter-methods of an analysis manager
    """

    @abstractmethod
    def get_analysis_types(self) -> [AnalysisTypeRecord]:
        """
        Gets the necessary parameter types from all analysis

        :return: A list of the type records
        """

        pass

    @abstractmethod
    def get_analysis_data(self, uuid: UUID) -> AnalysisDataRecord:
        """
        gets the analysis data record of the analysis with the given id
        """
        pass

    @abstractmethod
    def get_analysis_settings(self, uuid: UUID) -> AnalysisRecord:
        """
        gets the settings of the analysis with the given id
        """
        pass


class AnalysisManager(IAnalysisGetter, AbstractManager,
                      AnalysisFacadeConsumer, IAnalysisManager, FileFacadeConsumer):
    """
    The AnalysisManager implements the corresponding Interface. It makes use of the AnalysisFacade
    and the FileManager via the AnalysisFacadeConsumer and the FileManager. It structures the
    Handling of analysis internally.
    """

    def __init__(self):
        IAnalysisGetter.__init__(self)
        AbstractManager.__init__(self)
        AnalysisFacadeConsumer.__init__(self)
        IAnalysisManager.__init__(self)
        FileFacadeConsumer.__init__(self)

    def edit_analysis(self, analysis_id: UUID, analysis_record: AnalysisRecord) -> bool:
        if not self.analysis_facade.edit_analysis(analysis_id, analysis_record):
            self.handle_error([self.analysis_facade])
            return False
        self.events.append(AnalysisChanged(analysis_id))
        self.handle_event()
        return True

    @type_check(AnalysisTypeRecord)
    def add_analysis(self, analysis_type: AnalysisTypeRecord) -> bool:

        analysis_uuid = self.analysis_facade.create_analysis(analysis_type)
        if analysis_uuid is None:
            self.handle_error([self.analysis_facade])
            return False

        self.events.append(AnalysisAdded(analysis_uuid))
        self.handle_event()
        return True

    @type_check(UUID)
    def delete_analysis(self, uuid: UUID) -> bool:

        if not self._analysis_facade.delete_analysis(uuid):
            self.handle_error([self.analysis_facade])
            return False
        self.events.append(AnalysisDeleted(uuid))
        self.handle_event()
        return True

    @type_check(UUID)
    def refresh_analysis(self, uuid: UUID) -> bool:

        if not self._analysis_facade.refresh_analysis(uuid):
            self.handle_error([self.analysis_facade])
            return False

        self.events.append(AnalysisRefreshed(uuid))
        self.handle_event()
        return True

    @type_check(str)
    def import_analysis(self, path: str) -> bool:
        self.file_facade.import_new_analysis_to_standard_path(path)
        self.update_imported_analyses()
        return True

    def update_imported_analyses(self) -> bool:
        loaded_analysis_constructors: List[
            Callable[[], object]] = self.file_facade.get_analysis_types_from_standard_path()
        for loaded_constructor in loaded_analysis_constructors:
            analysis_type = self._analysis_facade.register_analysis_type(loaded_constructor)
            if analysis_type is None:
                self.handle_error([self.analysis_facade])
                return False
            self.events.append(AnalysisImported(analysis_type))
            self.handle_event()
        return True

    @type_check(UUID, AnalysisRecord)
    def edit_analysis_settings(self, uuid: UUID, analysis_setting: AnalysisRecord) -> bool:

        if not self._analysis_facade.edit_analysis(uuid, analysis_setting):
            self.handle_error([self.analysis_facade])
            return False
        self.events.append(AnalysisChanged(uuid))
        self.handle_event()
        return True

    @type_check(UUID)
    def get_analysis_settings(self, uuid: UUID) -> Optional[AnalysisRecord]:
        analysis_settings = self._analysis_facade.get_analysis_parameters(uuid)
        if analysis_settings is None:
            self.handle_error([self.analysis_facade])
            return None
        return analysis_settings

    def get_analysis_types(self) -> [AnalysisTypeRecord]:
        analysis_types = self._analysis_facade.get_analyses()
        if analysis_types is None:
            self.handle_error([self.analysis_facade])
            return []
        return analysis_types

    @type_check(UUID)
    def get_analysis_data(self, uuid: UUID) -> Optional[AnalysisDataRecord]:
        analysis_data = self._analysis_facade.get_analysed_data(uuid)
        if analysis_data is None:
            self.handle_error([self.analysis_facade])
            return None
        return analysis_data
