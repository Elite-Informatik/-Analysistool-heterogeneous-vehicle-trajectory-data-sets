from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

from src.controller.execution_handling.abstract_manager import AbstractManager
from src.controller.facade_consumer.data_facade_consumer import DataFacadeConsumer
from src.controller.facade_consumer.dataset_facade_consumer import DatasetFacadeConsumer
from src.controller.facade_consumer.file_facade_consumer import FileFacadeConsumer
from src.controller.output_handling.event import DatasetAdded
from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import DatasetOpened
from src.controller.output_handling.event import RefreshTrajectoryData
from src.data_transfer.content import COLUM_TO_VALUE_RANGE
from src.data_transfer.content import Column
from src.data_transfer.content import type_check
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import (InvalidInput)
from src.data_transfer.exception import InvalidUUID
from src.data_transfer.record import DataRecord
from src.data_transfer.record import DatasetRecord
from src.data_transfer.record import ErrorRecord
from src.data_transfer.record import SelectionRecord
from src.data_transfer.record import SettingContext
from src.data_transfer.record import SettingRecord
from src.data_transfer.selection import BoolDiscreteOption
from src.data_transfer.selection import DateIntervalOption
from src.data_transfer.selection import NumberIntervalOption
from src.data_transfer.selection import Option
from src.data_transfer.selection import TimeIntervalOption

DATA_EXISTS_SETTING: SettingRecord = SettingRecord.discrete_setting(setting_context="Data set already exists",
                                                                    options=["overwrite", "append"])


class IDatabaseManager(ABC):

    @abstractmethod
    def set_sql_connection(self, path: str) -> bool:
        """
        sets the sql connection
        :param path:    the path to the database
        :return:            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def initialize_datasets(self, dict_path: str) -> bool:
        """
        initializes the datasets
        :return:    True if successful, False otherwise
        """
        pass

    @abstractmethod
    def set_standard_paths(self, dict_path: str, data_path: str) -> bool:
        """
        sets the standard paths for the database
        :param dict_path:   the path to the dictionary
        :param data_path:   the path to the data
        :return:            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def open_dataset(self, uuid: UUID) -> bool:
        """
        opens a dataset with a given UUID
        :param uuid:    the UUID
        :return:        True if successful, False otherwise
        """
        pass

    @abstractmethod
    def save_datasets(self, dict_name: str) -> bool:
        """
        saves the datasets to a given dictionary
        :param dict_name:   the dictionary name
        :return:            True if successful, False otherwise
        """

    @abstractmethod
    def import_dataset(self, paths: List[str], name: str, file_format: str, mask_msg: bool = False) -> bool:
        """
        imports a dataset from a given path
        :param paths:       the paths to the files
        :param name:        the name of the dataset
        :param file_format: the file format of the files
        :param mask_msg:    True if the message should be masked, False otherwise
        :return:            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def load_datasets(self) -> bool:
        """
        loads the datasets from a given dictionary
        :param dataset_dict:    the dictionary
        :return:                True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_dataset(self, uuid: UUID) -> bool:
        """
        deletes a dataset with a given UUID
        :param uuid:    the UUID
        :return:        True if successful, False otherwise
        """
        pass


class IDatabaseGetter(ABC):

    @abstractmethod
    def get_discrete_selection_column(self, column: Column) -> Optional[SettingRecord]:
        """
        Returns a discrete option of all the possible parameters in the column that can
        be selected.
        :param column: The column of which the unique values will be returned.
        :return: An DiscreteOption containing the unique values.
        """
        pass

    @abstractmethod
    def get_interval_selection_column(self, column: Column) -> Optional[SettingRecord]:
        """
        Returns an interval option with the smallest and largest element of the column.
        :param column: The column of which the interval is constructed.
        :return: An interval option with the smallest and largest value of the column.
        """
        pass

    @abstractmethod
    def get_rawdata_trajectory(self, trajectory_id: UUID) -> Optional[DataRecord]:
        """
        gets the raw data of the trajectory with the given id
        :param trajectory_id:  the id of the trajectory
        :return:            the raw data
        """
        pass

    @abstractmethod
    def get_rawdata_datapoint(self, datapoint: UUID) -> Optional[DataRecord]:
        """
        gets the raw data of the datapoint with the given id
        :param datapoint:   the id of the datapoint
        :return:            the raw data
        """
        pass

    @abstractmethod
    def get_dataset_meta(self, dataset: UUID) -> Optional[DatasetRecord]:
        """
        gets the metadata of the dataset with the given id
        :param dataset:     the id of the dataset
        :return:            the metadata
        """
        pass

    @abstractmethod
    def get_rawdata(self, selected_column: List[Column]) -> Optional[DataRecord]:
        """
        gets the raw data of the selected columns
        :param selected_column: the selected columns
        :return:                the raw data
        """
        pass


class DatabaseManager(AbstractManager, DatasetFacadeConsumer, DataFacadeConsumer, FileFacadeConsumer,
                      IDatabaseGetter, IDatabaseManager):

    @type_check(str)
    def initialize_datasets(self, data_set_dict_path: str) -> bool:
        """
        Loads the saved datasets into the current state.
        """
        #todo: remove
        dataset_dict: Dict[str, int] = self.file_facade.import_dictionary_from_standard_path(
            data_set_dict_path)

        if dataset_dict is None:
            self.handle_error([self.file_facade])
            return False

        self.load_datasets()
        return True

    @type_check(str)
    def set_sql_connection(self, path: str) -> bool:
        sql_connection: Dict[str, str] = self.file_facade.import_dictionary_from_standard_path(path)
        if sql_connection is None:
            self.handle_error([self.file_facade])
            return False
        if not self.dataset_facade.set_connection(sql_connection):
            self.handle_error([self.dataset_facade])
            return False
        return True

    @type_check(Column)
    def get_discrete_selection_column(self, column: Column) -> Optional[SettingRecord]:

        if column not in Column.get_discrete_columns():
            self.request_manager.send_errors([ErrorRecord(ErrorMessage.INVALID_COLUMN_FILTER,
                                                          " discrete column was expected")])
            return None

        data_record: Optional[DataRecord] = self.data_facade.get_distinct_data_from_column(column)
        if data_record is None:
            self.handle_error([self.data_facade], " at getting discrete selection column in manager")
            return None
        distinct_values: List = data_record.data[column.value].to_list()

        return SettingRecord.discrete_setting(setting_context=SettingContext.DISCRETE.name,
                                              options=distinct_values)

    @type_check(Column)
    def get_interval_selection_column(self, column: Column) -> Optional[SettingRecord]:

        if column not in Column.get_interval_columns():
            self.request_manager.send_errors([ErrorRecord(ErrorMessage.INVALID_COLUMN_FILTER,
                                                          " interval column was expected")])
            return None

        # create interval option
        context: str
        interval_option: Option

        if column in Column.get_number_interval_columns():
            interval = COLUM_TO_VALUE_RANGE[column]
            interval_option = NumberIntervalOption(interval[0], interval[1])
            context = SettingContext.NUMBER_INTERVAL.name
            selected = [[0.0, 0.0]]
        elif column in Column.get_date_interval_columns():
            interval_option = DateIntervalOption()
            context = SettingContext.DATE_INTERVAL.name
            selected = [interval_option.get_option()]
        elif column in Column.get_time_interval_columns():
            interval_option = TimeIntervalOption()
            context = SettingContext.TIME_INTERVAL.name
            selected = [interval_option.get_option()]
        else:
            self.request_manager.send_errors([ErrorRecord(ErrorMessage.INVALID_COLUMN_FILTER,
                                                          " interval column was expected")])
            return None

        selection = SelectionRecord(selected=selected,
                                    option=interval_option,
                                    possible_selection_range=range(1, 2))

        # wrap interval in SettingRecord
        return SettingRecord(_context=context, _selection=selection)

    STANDARD_FAULT_ACCEPT: bool = False
    STANDARD_FAULT_NAME: str = "Dataset corrupted! \nContinue importing?\n"
    STANDARD_FAULT_OPTION: BoolDiscreteOption = BoolDiscreteOption()
    STANDARD_FAULT_SELECTION: SelectionRecord = SelectionRecord([False], STANDARD_FAULT_OPTION)

    @type_check(str, str)
    def set_standard_paths(self, dict_path: str, data_path: str) -> bool:
        if not self.file_facade.set_standard_paths(dictionary_standart_path=dict_path,
                                                   analysis_standart_path=data_path):
            self.handle_error([self.file_facade], " at setting standard paths in manager")
            return False
        return True

    @type_check(UUID)
    def open_dataset(self, uuid: UUID) -> bool:

        load_success: bool = self._dataset_facade.load_dataset(uuid)
        if self._dataset_facade.error_occurred() or not load_success:
            self.handle_error([self._dataset_facade], " at opening dataset in manager")
            return False

        self.events.append(DatasetOpened())
        self.events.append(RefreshTrajectoryData())
        self.handle_event()
        return True

    @type_check(str)
    def save_datasets(self, dict_name: str) -> bool:
        """
        Currently not used.
        """
        """dataset_dict = self.dataset_facade.get_data_sets_as_dict()

        if dataset_dict is None:
            self.handle_error([self.dataset_facade], " at exporting datasets in manager")
            return False

        if not self.file_facade.export_dictionary_to_standard_path(dict_name, dataset_dict):
            self.handle_error([self.file_facade], " at exporting datasets in manager")
            return False"""

        return True

    @type_check(List, str, str, bool)
    def import_dataset(self, paths: List[str], name: str, file_format: str, mask_msg: bool = False) -> bool:
        inaccuracies: List = []
        # import data and check for inaccuracies/ curruptions in the dataset
        allways_imported = paths[1:]
        chunked = paths[0]
        uuid = None
        self.file_facade.open_session(allways_imported, file_format)

        asked_innacuracies = False
        append: bool = False
        for i, imported_data in enumerate(self.file_facade.import_data_files(chunked, inaccuracies)):
            if imported_data is None:
                self.handle_error([self.file_facade])
                return False

            if len(inaccuracies) > 0 and not asked_innacuracies:
                # notify user about corruptions
                warning: str = str(ErrorMessage.DATASET_CORRUPTED.value)
                self.request_manager.send_warnings([warning])
                inaccuracy_str = ""
                for inaccuracy in inaccuracies:
                    inaccuracy_str += inaccuracy + "; "
                inaccuracy_str = inaccuracy_str[:-2]

                if not self.request_manager.ask_acceptance("The dataset contains the following corruptions: " +
                                                           inaccuracy_str, "Continue importing?"):
                    # cancel, if user does not accept corruptions
                    self.request_manager.send_errors([ErrorRecord(ErrorMessage.DATASET_CORRUPTED)])
                    return False
                asked_innacuracies = True

            imported_data: DataRecord = DataRecord(_name=name, _column_names=imported_data.column_names,
                                                   _data=imported_data.data)

            if i == 0:
                dataset_already_exists: bool = self.dataset_facade.table_exists(name)

                if dataset_already_exists:
                    # ask user if he wants to overwrite the dataset

                    list = ["overwrite", "append"]
                    setting = self.request_manager.request_selection(DATA_EXISTS_SETTING)

                    if setting is None or setting.selection.selected[0] == list[0]:
                        # cancel, if user does not want to overwrite
                        append = False
                    else:
                        append = True

            if i > 0:
                append = True

            uuid = self.dataset_facade.add_dataset(imported_data, append)
            if uuid is None and i == 0:
                self.handle_error([self.dataset_facade], " at importing dataset in manager")
                return False

        self.file_facade.close_session()

        if uuid is None or self.dataset_facade.error_occurred():
            self.handle_error([self.dataset_facade], " at importing dataset in manager")
        if uuid is None:
            return False

        if not mask_msg:
            self.request_manager.send_messages(["Import successful"]) # todo: why does this message not appear?
        self.events.append(DatasetAdded(uuid))
        self.handle_event()
        return True


    def load_datasets(self) -> bool:

        uuids: List[UUID] = self.dataset_facade.get_all_dataset_ids()

        for uuid in uuids:
            self.events.append(DatasetAdded(uuid))
        self.handle_event()
        return True

    @type_check(UUID)
    def delete_dataset(self, uuid: UUID) -> bool:

        if not self.dataset_facade.delete_dataset(uuid):
            self.handle_error([self.dataset_facade], " at deleting dataset in manager")
            return False

        self.request_manager.send_messages(["Deletion successful"])

        self.events.append(DatasetDeleted(uuid))
        self.handle_event()
        return True

    @type_check(UUID)
    def get_rawdata_trajectory(self, trajectory_id: UUID) -> Optional[DataRecord]:

        rawdata_trajectory = self._data_facade.get_data_of_column_selection(columns=Column.list(),
                                                                            filter_elements=[trajectory_id],
                                                                            filter_column=Column.TRAJECTORY_ID)

        return rawdata_trajectory

    @type_check(UUID)
    def get_rawdata_datapoint(self, datapoint: UUID) -> Optional[DataRecord]:

        data_of_column_selection = self._data_facade.get_data_of_column_selection(Column.list(), [datapoint], Column.ID)
        if data_of_column_selection is None:
            raise InvalidUUID("Datapoint with id " + str(datapoint) + " does not exist!")
        return data_of_column_selection

    @type_check(UUID)
    def get_dataset_meta(self, dataset: UUID) -> Optional[DatasetRecord]:
        record = self.dataset_facade.get_data_set_meta(dataset)
        if record is None:
            self.handle_error([self.dataset_facade], " at getting dataset meta in manager")
            return None

        return record

    @type_check(List)
    def get_rawdata(self, selected_column: List[Column]) -> Optional[DataRecord]:
        if selected_column is None:
            raise InvalidInput("Cannot select values from None column.")

        raw_data = self._data_facade.get_data(selected_column)
        if raw_data is None:
            self.handle_error([self._data_facade], " at getting rawdata in manager")
            return None

        return raw_data
