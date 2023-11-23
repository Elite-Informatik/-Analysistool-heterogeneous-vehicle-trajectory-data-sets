import os
from time import sleep
from typing import List
from unittest import TestCase
from uuid import UUID
from uuid import uuid4

import pandas
from sqlalchemy import create_engine

from src.controller.controller import Controller
from src.controller.execution_handling import database_manager
from src.controller.output_handling.abstract_event import *
from src.controller.output_handling.event import *
from src.data_transfer.content import Column
from src.data_transfer.content.data_types import DataTypes
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.exception import InvalidInput
from src.data_transfer.exception import InvalidUUID
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection import NumberIntervalOption
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.database.database import Database
from src.file.file_facade_manager import FileFacadeManager
from src.model.filter_structure.composite.filters.discrete_filter import DiscreteFilter
from src.model.filter_structure.composite.filters.interval_filter import IntervalFilter
from src.model.model import Model
from src.view.iview import IView
from src.view.view import IEventHandlerNotify
from src.view.view import UserInputRequestFacade


class BaseControllerTest(TestCase, UserInputRequestFacade, IEventHandlerNotify, IView):
    def setUp(self) -> None:
        current_dir = os.getcwd()
        print(current_dir)
        path, end = os.path.split(current_dir)
        while end != 'Analysetool':
            path, end = os.path.split(path)
            print(path, end)
        path = os.path.join(path, end)
        path = os.path.join(path, 'Analysetool')
        os.chdir(os.path.join(os.path.dirname(path), 'src'))

        self.started = False
        self.stopped = False

        self.events: List[Event] = list()
        self.event_types: List[object] = list()
        self.warnings: List[str] = list()
        self.errors: List[str] = list()
        self.messages: List[str] = list()
        self.selections: List[SettingRecord] = list()
        self.returned_selections: List[SettingRecord] = list()
        self.next_answer_to_ask_acceptance: List[bool] = []

        self.controller = Controller()

        model = Model()
        self.controller.set_model(model)

        database = Database()
        self.controller.set_database(database)

        self.file_adapter = FileFacadeManager()
        self.controller.set_file(self.file_adapter)

        model.set_controller(self.controller)
        self.controller.set_view(self)

    def user_input_request(self) -> UserInputRequestFacade:
        return self

    def event_handler(self) -> IEventHandlerNotify:
        return self

    def notify_event(self, event: Event):
        self.event_types.append(event.__class__)
        self.events.append(event)

    def send_warning(self, message: str):
        self.warnings.append(message)

    def send_error(self, message: str):
        self.errors.append(message)

    def send_message(self, message: str):
        self.messages.append(message)

    def ask_acceptance(self, message: str, accept_message="accept?", title: str = "") -> bool:
        if len(self.next_answer_to_ask_acceptance) == 0:
            self.fail("ask_acceptance was called but an answer was "
                      "not defined with next_answer_to_ask_acceptance list!")

        return self.next_answer_to_ask_acceptance.pop(0)

    def request_user_input(self, choice_setting: SettingRecord) -> SettingRecord:
        # self.selections.append(choice_setting)
        if len(self.returned_selections) == 0:
            print("request: ", choice_setting)
            self.fail("request_user_input was called more often than expected!")
        self.assertEqual(self.returned_selections[-1].context, choice_setting.context,
                         "request_user_input was called with an unexpected user input (setting)!")

        return self.returned_selections.pop()

    def expect_user_input(self, setting: SettingRecord):
        """
        Defines the expected user input. The user input is returned in the order of the calls to request_user_input.
        :param setting: the expected user input that is returned in the first call to request_user_input
        """
        self.returned_selections.append(setting)

    def remove_if_user_input_not_requested(self, setting: SettingRecord):
        """
        Removes the unnumbered user input if it was not requested. This is might be the case if a dataset does not exist
        when imported for example in which the user input is not needed.
        If on the other hand the dataset already exits the user input was requested.
        :param setting: the setting that might be removed
        """
        if len(self.returned_selections) != 0 and setting.context == self.returned_selections[-1].context \
                and setting.identifier == self.returned_selections[-1].identifier:
            self.returned_selections.pop()

    def check_event_types(self, event_types: List):
        self.assertEqual(len(event_types), len(self.events), "The number of events is not as expected! \n " +
                         "Expected: " + str(event_types) + "\n " +
                         "Real: " + str(self.event_types))
        for event_type, event, real_event_type in zip(event_types, self.events, self.event_types):
            self.assertEqual(event_type, real_event_type,
                             f"Method call with {real_event_type} was not expected! Expected: {event_type}")

            self.assertIsInstance(event, event_type)

    def check_errors(self, errors: List[str]):
        if len(errors) != len(self.errors):
            self.fail("The number of errors is not as expected! \n " +
                      "Expected: " + str(errors) + "\n " +
                      "Real: " + str(self.errors))
        for error, real_error in zip(errors, self.errors):
            self.assertEqual(error, real_error, f"Error was not expected! Expected: {error}")

    def check_warnings(self, warnings: List[str]):
        self.assertEqual(len(warnings), len(self.warnings))
        for warning, real_warning in zip(warnings, self.warnings):
            self.assertEqual(warning, real_warning, f"Warning was not expected! Expected: {warning}")

    def check_messages(self, messages: List[str]):
        self.assertEqual(len(messages), len(self.messages))
        for message, real_message in zip(messages, self.messages):
            self.assertEqual(message, real_message, f"Message was not expected! Expected: {message}")

    def assert_no_user_inputs(self):
        self.assertEqual(len(self.selections), 0, "request_user_input was unexpectedly called: " + str(self.selections))
        self.assertEqual(len(self.errors), 0, f"send_error was unexpectedly called with: {str(self.errors)}")
        self.assertEqual(len(self.messages), 0, "send_message was unexpectedly called with: " + str(self.messages))
        self.assertEqual(len(self.warnings), 0, "send_warning was unexpectedly called")
        # self.assertEqual(0, len(self.events), "notify_event was unexpectedly called")
        # self.assertEqual(0, len(self.event_types), "notify_event was unexpectedly called")

    def get_first_event(self) -> Event:
        self.event_types.pop()
        return self.events.pop()

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True


class StartedStoppedControllerTest(BaseControllerTest):
    def setUp(self) -> None:
        super().setUp()
        self.controller.application_command_facade.start()
        self.events = []
        self.event_types = []
        self.open_datasets = []
        self.duplicate_dataset_setting = database_manager.DATA_EXISTS_SETTING

    def tearDown(self) -> None:
        self.events = []
        self.event_types = []
        for dataset in self.open_datasets:
            self.delete_dataset(dataset, remove_from_list=False)
        self.open_datasets = []
        self.assert_no_user_inputs()
        self.controller.application_command_facade.stop()
        super().tearDown()

    def delete_dataset(self, dataset_id: UUID, remove_from_list: bool = True):
        """
        Deletes a dataset and checks if the dataset was deleted correctly.
        @param dataset_id: the id of the dataset that should be deleted
        @param remove_from_list: if the dataset should be removed from the list of open datasets
        @return:
        """
        self.controller.communication_facade.delete_dataset(dataset_id)
        if remove_from_list:
            self.open_datasets.remove(dataset_id)
        self.check_event_types([DatasetDeleted])
        self.get_first_event()
        self.check_messages(["Deletion successful"])
        self.messages.pop()

    def open_dataset(self, paths: List[str], dataset_type: str, name: str = "test_data") -> None:
        """
        Opens a dataset and checks if the dataset was opened correctly. It also checks for unexpected events, such as
        events that were not requested, errors, warnings and messages.
        :param paths: the paths to the files that should be imported
        :param dataset_type: the type of the dataset that should be imported
        :param name: the name of the dataset that it will be imported as
        :return: None
        """
        sleep(0.1)
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))

        self.expect_user_input(self.duplicate_dataset_setting)
        self.controller.communication_facade.import_dataset(paths, name, dataset_type)
        self.check_errors([])
        self.remove_if_user_input_not_requested(self.duplicate_dataset_setting)

        self.check_event_types([DatasetAdded])
        self.dataset_uuid = self.get_first_event().id
        self.controller.communication_facade.open_dataset(self.dataset_uuid)
        self.check_event_types([DatasetOpened, RefreshTrajectoryData])
        self.open_datasets.append(self.dataset_uuid)
        for i in range(2):
            self.get_first_event()
        self.check_messages(["Import successful"])
        self.messages.pop()
        self.assert_no_user_inputs()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'src'))

    def open_dataset_intern(self, path: str, name="test_data") -> None:
        """
        Opens a dataset of type intern at the given path.
        :param path: the path to the dataset
        :param name: the name of the dataset
        :return: None
        """
        self.open_dataset([path], "intern", name=name)

    def open_dataset_fcd_ui(self, path: str) -> None:
        """
        Opens a dataset of type FCD UI at the given path.
        :param path: the path to the dataset
        :return: None
        """
        self.open_dataset([path], "FCD UI")

    def open_dataset_simra_bicycle(self, path: str):
        """
        Opens a dataset of type SimRa Bicycle at the given path.
        :param path: the path to the dataset
        :return: None
        """
        self.open_dataset([path], "SimRa")

    def open_dataset_highD(self, path: [str]) -> None:
        """
        Opens a dataset of type HighD at the given path.
        :param path: the path to the dataset
        :return: None
        """
        self.assertEqual(3, len(path), "The path to the HighD dataset must contain 3 files (data, meta, config)")
        self.open_dataset(path, DataTypes.HIGH_D.value)


class TestControllerStartStopCommands(BaseControllerTest):
    def start_controller(self):
        with self.subTest("start command"):
            self.controller.application_command_facade.start()
            self.assertTrue(self.started)
            self.assertFalse(self.stopped)

        with self.subTest("check events"):
            self.number_of_analysises = len(
                os.listdir(os.path.join(os.getcwd(), "model/analysis_structure/concrete_analysis"))) - 1

            datasets = self.controller._database.dataset_facade.get_all_dataset_ids()
            self.number_of_datasets = len(datasets)

            events = [DatasetAdded] * self.number_of_datasets
            events2 = [AnalysisImported] * self.number_of_analysises
            events.extend(events2)

            self.check_event_types(events)

        self.assert_no_user_inputs()

    def stop_controller(self):
        with self.subTest("stop command"):
            self.controller.application_command_facade.stop()
            # self.assertTrue(self.stopped) TODO: fix this
            self.assert_no_user_inputs()

    def test_start_stop_command(self):
        self.start_controller()
        self.stop_controller()


class OpenInternDatasetControllerTest(StartedStoppedControllerTest):
    def setUp(self) -> None:
        super().setUp()
        self.open_dataset_intern(path="file/data_for_tests/intern_data.csv")


# -------------------------------------------------------------------- #
#                                                                      #
#                             Polygone                                 #
#                                                                      #
# -------------------------------------------------------------------- #

class PolygonControllerTest(StartedStoppedControllerTest):
    def setUp(self) -> None:
        super().setUp()
        self.polygon1 = PolygonRecord((PositionRecord(0, 0), PositionRecord(1, 0), PositionRecord(0, 1)),
                                      "poly das polygon")
        self.polygon2 = PolygonRecord((PositionRecord(1, 1), PositionRecord(1, 2), PositionRecord(2, 1)),
                                      "poly das polygon")
        self.badpolygons: [PolygonRecord] = [
            PolygonRecord((), "aaaa"),  # too few points
            PolygonRecord((
                PositionRecord(20, 20),
                PositionRecord(30, 30),
                PositionRecord(91, -1)), _name="valid _name"),  # invalid coordinate
            PolygonRecord((
                PositionRecord(20, 20),
                PositionRecord(20, 30),
                PositionRecord(10, 10)), _name="")  # illegal _name
        ]
        self.badpolygons_errors = {self.badpolygons[0]: ErrorMessage.POLYGON_TOO_FEW_POINTS,
                                   self.badpolygons[1]: ErrorMessage.POLYGON_ILLEGAL_COORDINATES,
                                   self.badpolygons[2]: ErrorMessage.INVALID_NAME}


class TestAddPolygonCommand(PolygonControllerTest):
    def test_add_polygon(self):
        with self.subTest("add polygon"):
            self.controller.communication_facade.add_polygon(self.polygon1)
            self.check_event_types([PolygonAdded])
            self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 1,
                             "Wrong amount of Polygons created")

        with self.subTest("check polygon"):
            polygon_das_polygon = self.controller.data_request_facade.get_polygon(self.get_first_event().id)
            self.assertEqual(self.polygon1, polygon_das_polygon)

        with self.subTest("add invalid polygon"):
            self.assertRaises(InvalidInput, self.controller.communication_facade.add_polygon, None)
            self.check_event_types([])

        with self.subTest("add bad polygons"):
            for bad_polygon in self.badpolygons:
                self.controller.communication_facade.add_polygon(bad_polygon)

                with self.subTest("Check error message"):
                    self.assertEqual(self.errors.pop(), self.badpolygons_errors[bad_polygon].value)
            self.check_event_types([])

        with self.subTest("Undo add polygon"):
            self.controller.communication_facade.undo()
            self.check_event_types([PolygonDeleted])
            self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 0,
                             "Adding Polygon not undone")
            self.get_first_event()

        with self.subTest("Redo add polygon"):
            self.controller.communication_facade.redo()
            polygon_das_polygon_id = self.get_first_event().id
            polygon_das_polygon = self.controller.data_request_facade.get_polygon(polygon_das_polygon_id)
            self.assertEqual(self.polygon1, polygon_das_polygon)
            self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 1,
                             "Wrong amount of Polygons created")


class TestRedoAddPolygonCommand(PolygonControllerTest):
    def test_add_polygon2(self):
        self.controller.communication_facade.add_polygon(self.polygon1)
        self.controller.communication_facade.add_polygon(self.polygon2)
        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 2)
        self.controller.communication_facade.undo()
        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 1)
        self.controller.communication_facade.undo()
        self.assertEqual(self.controller.data_request_facade.get_polygon_ids(), [])
        self.controller.communication_facade.redo()
        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 1)
        self.controller.communication_facade.redo()
        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 2)

        self.check_event_types([PolygonAdded, PolygonAdded, PolygonDeleted, PolygonDeleted, PolygonAdded, PolygonAdded])
        polygon_das_polygon = self.controller.data_request_facade.get_polygon(
            self.controller.data_request_facade.get_polygon_ids()[0])
        self.assertEqual(self.polygon1, polygon_das_polygon)
        polygon_das_polygon = self.controller.data_request_facade.get_polygon(
            self.controller.data_request_facade.get_polygon_ids()[1])
        self.assertEqual(self.polygon2, polygon_das_polygon)
        self.events = self.events[0:4]
        for i in range(4):
            self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_polygon, self.events.pop().id)

        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 2,
                         "Wrong amount of Polygons created")

    def test_add_polygon3(self):
        self.controller.communication_facade.add_polygon(self.polygon1)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.controller.communication_facade.add_polygon(self.polygon2)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()

        self.check_event_types([PolygonAdded, PolygonDeleted, PolygonAdded, PolygonAdded, PolygonDeleted, PolygonAdded])
        polygon_das_polygon = self.controller.data_request_facade.get_polygon(self.events.pop(5).id)
        self.assertEqual(self.polygon2, polygon_das_polygon)
        polygon_das_polygon = self.controller.data_request_facade.get_polygon(self.events.pop(2).id)
        self.assertEqual(self.polygon1, polygon_das_polygon)
        for i in range(4):
            self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_polygon, self.events.pop().id)

        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 2,
                         "Wrong amount of Polygons created")


class TestDeletePolygonCommand(PolygonControllerTest):
    def test_delete_polygon(self):
        self.controller.communication_facade.add_polygon(self.polygon1)
        self.controller.communication_facade.delete_polygon(self.events[0].id)

        self.check_event_types([PolygonAdded, PolygonDeleted])
        for i in range(2):
            self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_polygon, self.events.pop().id)

        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 0,
                         "Wrong amount of Polygons created")

    def test_delete_non_existend_polygon(self):
        with self.assertRaises(InvalidUUID):
            self.controller.communication_facade.delete_polygon(uuid4())

    def test_delete_none_polygon(self):
        with self.assertRaises(InvalidUUID):
            self.controller.communication_facade.delete_polygon(None)


class TestUndoDeletePolygonCommand(PolygonControllerTest):
    def test_delete_polygon(self):
        self.controller.communication_facade.add_polygon(self.polygon1)
        self.controller.communication_facade.delete_polygon(self.events[0].id)
        self.controller.communication_facade.undo()
        self.check_event_types([PolygonAdded, PolygonDeleted, PolygonAdded])
        for i in range(3):
            polygon_das_polygon = self.controller.data_request_facade.get_polygon(self.events.pop().id)
            self.assertEqual(self.polygon1, polygon_das_polygon)
        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 1,
                         "Wrong amount of Polygons created")


class TestRedoDeletePolygonCommand(PolygonControllerTest):
    def test_delete_polygon(self):
        self.controller.communication_facade.add_polygon(self.polygon1)
        self.controller.communication_facade.delete_polygon(self.events[0].id)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.check_event_types([PolygonAdded, PolygonDeleted, PolygonAdded, PolygonDeleted])
        for i in range(4):
            self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_polygon, self.events.pop().id)

        self.assertEqual(len(self.controller.data_request_facade.get_polygon_ids()), 0,
                         "Wrong amount of Polygons created")


# -------------------------------------------------------------------- #
#                                                                      #
#                              Filter                                  #
#                                                                      #
# -------------------------------------------------------------------- #

class FilterControllerTest(OpenInternDatasetControllerTest):
    def setUp(self) -> None:
        super().setUp()
        self.polygon1 = PolygonRecord((PositionRecord(0, 0), PositionRecord(1, 0), PositionRecord(0, 1)),
                                      "poly das polygon")
        self.polygon2 = PolygonRecord((PositionRecord(1, 1), PositionRecord(1, 2), PositionRecord(2, 1)),
                                      "poly das polygon")
        filter_types = self.controller.data_request_facade.get_filter_types()

        for filter_type in filter_types:
            filter_selection = self.controller.data_request_facade.get_filter_selections(filter_type)
            self.assertIsNotNone(filter_selection)

        self.controller.data_request_facade.get_filter_group_selection()

        self.filter_record_interval1 = FilterRecord(
            _name="filtixx",
            _negated=True,
            _enabled=True,
            _structure_name="point filters",
            _type="interval filter",
            _interval_setting=SettingRecord(
                _context="Select Interval for Interval Filter",
                _selection=SelectionRecord(
                    selected=[[1, 1000]],
                    option=NumberIntervalOption(1, 1000),
                    possible_selection_range=range(1, 3)
                ),
                _identifier=SettingsEnum.INTERVAL
            ),
            _column_setting=SettingRecord(
                _context="Select Column for Interval Filter",
                _selection=SelectionRecord(
                    selected=[Column.SPEED_LIMIT],
                    option=DiscreteOption(
                        options=IntervalFilter.APPLYABLE_COLUMNS
                    )
                ),
                _identifier=SettingsEnum.COLUMN
            ),
            _polygon_setting=None,
            _discrete_setting=None
        )

        self.filter_record_interval2 = FilterRecord(
            _name="filtiyyy",
            _negated=False,
            _enabled=True,
            _structure_name="point filters",
            _type="interval filter",
            _interval_setting=SettingRecord(
                _context="Select Interval for Interval Filter",
                _selection=SelectionRecord(
                    selected=[[1, 12]],
                    option=NumberIntervalOption(1, 12),
                    possible_selection_range=range(1, 2)
                ),
                _identifier=SettingsEnum.INTERVAL
            ),

            _column_setting=SettingRecord(
                _context="Select Column for Interval Filter",
                _selection=SelectionRecord(
                    selected=[Column.SPEED],
                    option=DiscreteOption(
                        options=IntervalFilter.APPLYABLE_COLUMNS
                    )
                ),
                _identifier=SettingsEnum.COLUMN
            ),
            _polygon_setting=None,
            _discrete_setting=None
        )

        self.filter_record_discrete1 = FilterRecord(
            _name="filter",
            _negated=True,
            _enabled=True,
            _structure_name="point filters",
            _type="discrete filter",
            _discrete_setting=SettingRecord(
                _selection=SelectionRecord(
                    selected=["Berg", "Tal"],
                    option=DiscreteOption(options=["Berg", "Tal"]),
                    possible_selection_range=range(0, 3)
                ),
                _context='Select Values for Discrete Filter',
                _identifier=SettingsEnum.DISCRETE
            ),
            _column_setting=SettingRecord(
                _selection=SelectionRecord(
                    selected=[Column.TRAJECTORY_ID],
                    option=DiscreteOption(
                        options=DiscreteFilter.APPLYABLE_COLUMNS
                    )
                ),
                _context='Select Column for Discrete Filter',
                _identifier=SettingsEnum.COLUMN
            ),
            _polygon_setting=None,
            _interval_setting=None
        )

        self.filter2 = None
        self.filter_group_record1 = FilterGroupRecord(
            _name='aaa',
            _structure_name='point filters',
            _enabled=True,
            _negated=False,
            _operator=LogicalOperator.OR.name,
            _filter_records=tuple()
        )
        self.filter_group_record2 = FilterGroupRecord(
            _name='aba',
            _structure_name='point filters',
            _enabled=False,
            _negated=True,
            _operator=LogicalOperator.AND.name,
            _filter_records=tuple()
        )


class TestAddFilterGroupCommand(FilterControllerTest):
    def test_add_filter_group(self):
        with self.subTest("filter types"):
            self.assertIsNotNone(self.controller.data_request_facade.get_filter_types())

        with self.subTest("check root"):
            self.assertIsNotNone(self.controller.data_request_facade.get_point_filters_root())

        with self.subTest("add filter group"):
            root_id = self.controller.data_request_facade.get_point_filters_root()
            self.assertIsNotNone(root_id)

        with self.subTest("add filter group"):
            self.controller.communication_facade.add_filter_group(
                filter_group=self.filter_group_record1,
                parent=root_id
            )
            self.check_event_types([FilterGroupAdded, RefreshTrajectoryData])
            self.get_first_event()
            group_id = self.get_first_event().id
            group_new = self.controller.data_request_facade.get_filter_group(group_id)
            self.assertEqual(group_new, self.filter_group_record1)

    def test_add_filter_group2(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=group_id

        )
        self.check_event_types([FilterGroupAdded, RefreshTrajectoryData])
        self.get_first_event()
        group_id = self.get_first_event().id
        group_new = self.controller.data_request_facade.get_filter_group(group_id)
        self.assertEqual(group_new, self.filter_group_record1)


class TestUndoAddFilterGroupCommand(FilterControllerTest):
    def test_undo_add_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.undo()
        self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_filter_group, group_id)
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData])


class TestRedoAddFilterGroupCommand(FilterControllerTest):
    def test_redo_add_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        self.get_first_event()
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData, FilterGroupAdded, RefreshTrajectoryData])
        self.get_first_event()
        group_id = self.get_first_event().id
        self.get_first_event()
        self.get_first_event()
        group_new = self.controller.data_request_facade.get_filter_group(group_id)
        self.assertEqual(group_new, self.filter_group_record1)


class TestDeleteFilterGroupCommand(FilterControllerTest):
    def test_delete_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.delete_filter_group(group_id)
        self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_filter_group, group_id)
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData])

    def try_deleting_root_id(self, root_getter, error: ErrorMessage):
        self.controller.communication_facade.delete_filter_group(root_getter())
        root_id = root_getter()
        self.assertIsNotNone(root_id)
        self.assertIsNotNone(self.controller.data_request_facade.get_filter_group(root_id))
        self.assertEqual(self.errors.pop(), error.value)

    def test_delete_root_filter_group(self):
        root_getters = [
            self.controller.data_request_facade.get_point_filters_root,
            self.controller.data_request_facade.get_trajectory_filters_root
        ]
        for root_getter in root_getters:
            self.try_deleting_root_id(root_getter, ErrorMessage.FILTER_NOT_DELETED)

        root_id1 = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id1
        )

        for root_getter in root_getters:
            self.try_deleting_root_id(root_getter, ErrorMessage.FILTER_NOT_DELETED)


class TestUndoDeleteFilterGroupCommand(FilterControllerTest):
    def test_undo_delete_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.delete_filter_group(group_id)
        self.controller.communication_facade.undo()

        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData, FilterGroupAdded, RefreshTrajectoryData])
        self.get_first_event()
        group_id = self.get_first_event().id
        group_new = self.controller.data_request_facade.get_filter_group(group_id)
        self.assertEqual(group_new, self.filter_group_record1)


class TestRedoDeleteFilterGroupCommand(FilterControllerTest):
    def test_redo_delete_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.delete_filter_group(group_id)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_filter_group, group_id)
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData, FilterGroupAdded, RefreshTrajectoryData,
                                FilterComponentDeleted, RefreshTrajectoryData])


class TestChangeFilterGroupCommand(FilterControllerTest):
    def test_change_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.change_filter_group(
            group_id=group_id,
            filter_group=self.filter_group_record2
        )
        self.assertEqual(
            self.filter_group_record2,
            self.controller.data_request_facade.get_filter_group(group_id)
        )
        self.check_event_types([FilterGroupChanged, RefreshTrajectoryData])


class TestUndoChangeFilterGroupCommand(FilterControllerTest):
    def test_undo_change_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.change_filter_group(
            group_id=group_id,
            filter_group=self.filter_group_record2
        )
        self.controller.communication_facade.undo()
        self.assertEqual(
            self.filter_group_record1,
            self.controller.data_request_facade.get_filter_group(group_id)
        )
        self.check_event_types([FilterGroupChanged, RefreshTrajectoryData, FilterGroupChanged, RefreshTrajectoryData])


class TestRedoChangeFilterGroupCommand(FilterControllerTest):
    def test_redo_change_filter_group(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter_group(
            filter_group=self.filter_group_record1,
            parent=root_id
        )
        self.get_first_event()
        group_id = self.get_first_event().id
        self.controller.communication_facade.change_filter_group(
            filter_group=self.filter_group_record2,
            group_id=group_id
        )
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.assertEqual(
            self.filter_group_record2,
            self.controller.data_request_facade.get_filter_group(group_id)
        )
        self.check_event_types([FilterGroupChanged, RefreshTrajectoryData, FilterGroupChanged, RefreshTrajectoryData,
                                FilterGroupChanged, RefreshTrajectoryData])


class TestAddFilterCommand(FilterControllerTest):
    def test_add_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_discrete1, root_id)
        self.check_event_types([FilterAdded, RefreshTrajectoryData])
        self.get_first_event()
        filter_id = self.get_first_event().id
        filter_new = self.controller.data_request_facade.get_filter(filter_id)
        self.assertEqual(
            self.filter_record_discrete1,
            filter_new
        )


class TestUndoAddFilterCommand(FilterControllerTest):
    def test_undo_add_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_discrete1, root_id)
        self.controller.communication_facade.undo()
        self.check_event_types([FilterAdded, RefreshTrajectoryData, FilterComponentDeleted, RefreshTrajectoryData])
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_filter_group, filter_id)


class TestRedoAddFilterCommand(FilterControllerTest):
    def test_redo_add_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_discrete1, root_id)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.check_event_types([FilterAdded, RefreshTrajectoryData, FilterComponentDeleted, RefreshTrajectoryData,
                                FilterAdded, RefreshTrajectoryData])
        self.get_first_event()
        filter_id = self.get_first_event().id
        filter_new = self.controller.data_request_facade.get_filter(filter_id)

        self.assertEqual(
            self.filter_record_discrete1,
            filter_new
        )


class TestChangeFilterCommand(FilterControllerTest):
    def test_change_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_interval1, root_id)
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.controller.communication_facade.change_filter(filter_id, self.filter_record_interval2)
        self.check_event_types([FilterChanged, RefreshTrajectoryData])
        self.controller.data_request_facade.get_filter(filter_id)
        filter_record = self.controller.data_request_facade.get_filter(filter_id)
        self.filter_record_interval2._interval_setting.selection._possible_selection_amount = \
            filter_record.intervall.selection.possible_selection_amount
        self.assertEqual(self.filter_record_interval2, filter_record)


class TestUnodChangeFilterCommand(FilterControllerTest):
    def test_undo_change_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_interval1, root_id)
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.controller.communication_facade.change_filter(filter_id, self.filter_record_interval2)
        self.controller.communication_facade.undo()
        self.check_event_types([FilterChanged, RefreshTrajectoryData, FilterChanged, RefreshTrajectoryData])
        self.controller.data_request_facade.get_filter(filter_id)
        filter_record = self.controller.data_request_facade.get_filter(filter_id)
        self.filter_record_interval1._interval_setting.selection._possible_selection_amount = \
            filter_record.intervall.selection.possible_selection_amount
        self.assertEqual(filter_record, self.filter_record_interval1)


class TestRedoChangeFilterCommand(FilterControllerTest):
    def test_redo_change_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_interval1, root_id)
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.controller.communication_facade.change_filter(filter_id, self.filter_record_interval2)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.check_event_types([FilterChanged, RefreshTrajectoryData, FilterChanged, RefreshTrajectoryData,
                                FilterChanged, RefreshTrajectoryData])
        filter_record = self.controller.data_request_facade.get_filter(filter_id)
        self.filter_record_interval2._interval_setting.selection._possible_selection_amount = \
            filter_record.intervall.selection.possible_selection_amount
        self.assertEqual(filter_record, self.filter_record_interval2)


class TestDeleteFilterCommand(FilterControllerTest):
    def test_delete_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_interval1, root_id)
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.controller.communication_facade.delete_filter(filter_id)
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData])
        self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_filter, filter_id)


class TestUndoDeleteFilter(FilterControllerTest):
    def test_undo_delete_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_interval2, root_id)
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.controller.communication_facade.delete_filter(filter_id)
        self.controller.communication_facade.undo()
        filter_record = self.controller.data_request_facade.get_filter(filter_id)
        self.filter_record_interval2._interval_setting.selection._possible_selection_amount = \
            filter_record.intervall.selection.possible_selection_amount
        self.assertEqual(filter_record, self.filter_record_interval2)
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData, FilterAdded, RefreshTrajectoryData])


class TestRedoDeleteFilter(FilterControllerTest):
    def test_redo_delete_filter(self):
        root_id = self.controller.data_request_facade.get_point_filters_root()
        self.controller.communication_facade.add_filter(self.filter_record_interval2, root_id)
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.controller.communication_facade.delete_filter(filter_id)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_filter, filter_id)
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData, FilterAdded, RefreshTrajectoryData,
                                FilterComponentDeleted, RefreshTrajectoryData])


# -------------------------------------------------------------------- #
#                                                                      #
#                             Analysen                                 #
#                                                                      #
# -------------------------------------------------------------------- #

class AnalysisConrollerTest(StartedStoppedControllerTest):
    def setUp(self) -> None:
        super().setUp()
        self.polygon1 = PolygonRecord((PositionRecord(0, 0), PositionRecord(1, 0), PositionRecord(0, 1)),
                                      "poly das polygon")
        self.controller.communication_facade.add_polygon(self.polygon1)
        self.get_first_event()


class TestImportAnalysis(AnalysisConrollerTest):
    def test_import_analysis(self):
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))
        self.controller.communication_facade.import_analysis_type(
            os.path.join(os.getcwd(), "model/analysis_structure/dummy_analysis.py"))

    def tearDown(self) -> None:
        super().tearDown()
        # removes the dummy analysis again
        os.chdir(self.current_dir)
        os.remove(os.path.join(os.getcwd(), "model/analysis_structure/concrete_analysis/dummy_analysis.py"))


class TestAddAnalysis(AnalysisConrollerTest):
    def test_add_analysis(self):
        analysis_types = self.controller.data_request_facade.get_analysis_types()
        self.assertIsNotNone(analysis_types)
        for analysis_type in analysis_types:
            self.assertIsNotNone(analysis_type)
            self.controller.communication_facade.add_analysis(analysis_type)
            self.check_event_types([AnalysisAdded])
            analysis_id = self.get_first_event().id
            self.assertIsNotNone(analysis_id)
            analysis_settings = self.controller.data_request_facade.get_analysis_settings(analysis_id)
            self.assertIsNotNone(analysis_settings)


class TestDeleteAnalysis(AnalysisConrollerTest):
    def test_delete_analysis(self):
        analysis_types = self.controller.data_request_facade.get_analysis_types()
        for analysis_type in analysis_types:
            self.assertIsNotNone(analysis_type)
            self.controller.communication_facade.add_analysis(analysis_type)
            analysis_id = self.get_first_event().id
            self.controller.communication_facade.delete_analysis(analysis_id)
            self.assertRaises(InvalidUUID, self.controller.data_request_facade.get_analysis_settings, analysis_id)


class TestChangeAnalysis(AnalysisConrollerTest):
    def test_change_analysis(self):
        analysis_types = self.controller.data_request_facade.get_analysis_types()
        analysis_type_path_time = None
        for analysis_type in analysis_types:
            if analysis_type.name == "table":
                analysis_type_path_time = analysis_type
        self.assertIsNotNone(analysis_type_path_time)
        self.controller.communication_facade.add_analysis(analysis_type_path_time)
        analysis_id = self.get_first_event().id
        analysis1 = self.controller.data_request_facade.get_analysis_settings(analysis_id)
        analysis2 = AnalysisRecord((SettingRecord(
            _identifier=SettingsEnum.DEF_SETTING,
            _context="columns",
            _selection=SelectionRecord(
                selected=[Column.ID.value, Column.TRAJECTORY_ID.value, Column.DATE.value, Column.LONGITUDE.value,
                          Column.LATITUDE.value, Column.SPEED.value, Column.ACCELERATION.value],
                option=DiscreteOption(Column.val_list()),
                possible_selection_range=range(1, len(Column.list()) + 1)
            )
        ),
        ))
        print(analysis2.required_data[0], analysis1.required_data[0])
        self.assertEqual(analysis2.required_data[0], analysis1.required_data[0])
        self.assertEqual(analysis2, analysis1)
        analysis3 = AnalysisRecord((SettingRecord(
            _context="columns",
            _selection=SelectionRecord(
                selected=[Column.TRAJECTORY_ID.value, Column.SPEED_LIMIT.value, Column.OSM_ROAD_ID.value],
                option=DiscreteOption(Column.val_list()),
                possible_selection_range=range(1, len(Column.list()) + 1)
            )
        ),
        ))
        self.controller.communication_facade.change_analysis(analysis_id, analysis3)
        self.check_event_types([AnalysisChanged])
        analysis_id = self.get_first_event().id

        self.assertEqual(
            self.controller.data_request_facade.get_analysis_settings(analysis_id),
            analysis3
        )


class TestUndoChangeAnalysis(AnalysisConrollerTest):
    def test_undo_change_analysis(self):
        analysis_types = self.controller.data_request_facade.get_analysis_types()
        analysis_type_path_time = None
        for analysis_type in analysis_types:
            if analysis_type.name == "table":
                analysis_type_path_time = analysis_type
        self.assertIsNotNone(analysis_type_path_time)
        self.controller.communication_facade.add_analysis(analysis_type_path_time)
        analysis_id = self.get_first_event().id
        analysis3 = AnalysisRecord((SettingRecord(
            _identifier=SettingsEnum.DEF_SETTING,
            _context="columns",
            _selection=SelectionRecord(
                selected=[Column.TRAJECTORY_ID.value, Column.SPEED_LIMIT.value, Column.OSM_ROAD_ID.value],
                option=DiscreteOption(Column.val_list()),
                possible_selection_range=range(1, len(Column.val_list()) + 1)
            )
        ),
        ))
        analysis1 = self.controller.data_request_facade.get_analysis_settings(analysis_id)
        self.controller.communication_facade.change_analysis(analysis_id, analysis3)
        self.controller.communication_facade.undo()
        self.check_event_types([AnalysisChanged, AnalysisChanged])
        self.assertEqual(
            self.controller.data_request_facade.get_analysis_settings(analysis_id),
            analysis1
        )


class TestRedoChangeAnalysis(AnalysisConrollerTest):
    def test_redo_change_analysis(self):
        analysis_types = self.controller.data_request_facade.get_analysis_types()
        analysis_type_path_time = None
        for analysis_type in analysis_types:
            if analysis_type.name == "table":
                analysis_type_path_time = analysis_type
        self.assertIsNotNone(analysis_type_path_time)
        self.controller.communication_facade.add_analysis(analysis_type_path_time)
        analysis_id = self.get_first_event().id
        analysis3 = AnalysisRecord((SettingRecord(
            _identifier=SettingsEnum.DEF_SETTING,
            _context="columns",
            _selection=SelectionRecord(
                selected=[Column.TRAJECTORY_ID.value, Column.SPEED_LIMIT.value, Column.OSM_ROAD_ID.value],
                option=DiscreteOption(Column.val_list()),
                possible_selection_range=range(1, len(Column.val_list()) + 1)
            )
        ),
        ))
        self.controller.communication_facade.change_analysis(analysis_id, analysis3)
        self.controller.communication_facade.undo()
        self.controller.communication_facade.redo()
        self.check_event_types([AnalysisChanged, AnalysisChanged, AnalysisChanged])
        self.assertEqual(
            self.controller.data_request_facade.get_analysis_settings(analysis_id),
            analysis3
        )


# -------------------------------------------------------------------- #
#                                                                      #
#                             Settings                                 #
#                                                                      #
# -------------------------------------------------------------------- #

class SettingControllerTest(StartedStoppedControllerTest):
    def setUp(self) -> None:
        super().setUp()
        self.settings = self.controller.data_request_facade.get_settings()


class TestChangeSettingsCommand(SettingControllerTest):
    def test_change_settings(self):
        self.settings.change(SettingsEnum.SHOW_LINE_SEGMENTS, False)
        self.controller.communication_facade.change_settings(self.settings)
        self.assertEqual(
            self.controller.data_request_facade.get_settings(),
            self.settings
        )
        self.check_event_types([SettingsChanged])


class TestUndoChangeSettingsCommand(SettingControllerTest):
    def test_change_settings(self):
        self.settings.change(SettingsEnum.SHOW_LINE_SEGMENTS, False)
        self.controller.communication_facade.change_settings(self.settings)
        self.controller.communication_facade.undo()
        self.assertEqual(
            self.controller.data_request_facade.get_settings(),
            self.settings
        )
        self.check_event_types([SettingsChanged, SettingsChanged])


# -------------------------------------------------------------------- #
#                                                                      #
#                             Datasets                                 #
#                                                                      #
# -------------------------------------------------------------------- #

class TestImportDataset(StartedStoppedControllerTest):
    def test_import_dataset(self):
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))
        self.controller.communication_facade.import_dataset(["file/data_for_tests/intern_data.csv"],
                                                            "test_data", "intern")
        self.check_event_types([DatasetAdded])
        self.assertEqual(len(self.messages), 1)
        self.messages.pop()
        uuid = self.events.pop().id
        self.controller.communication_facade.delete_dataset(uuid)
        self.messages.pop()


class TestDeleteDataset(StartedStoppedControllerTest):
    def test_delete_dataset(self):
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))
        self.controller.communication_facade.import_dataset(["file/data_for_tests/intern_data.csv"],
                                                            "test_data", "intern")
        uuid = self.get_first_event().id
        self.assertEqual(len(self.messages), 1)
        self.messages.pop()
        self.controller.data_request_facade.get_dataset_meta(uuid)
        self.delete_dataset(uuid)

        self._check_dataset_not_existing(uuid)

    def delete_dataset(self, uuid: UUID):
        self.controller.communication_facade.delete_dataset(uuid)
        self.check_event_types([DatasetDeleted])
        self.assertIsNotNone(self.get_first_event().id)
        self.assertIsNotNone(self.messages.pop())

        self._check_dataset_not_existing(uuid)

    def _check_dataset_not_existing(self, uuid: UUID):
        self.controller.data_request_facade.get_dataset_meta(uuid)
        if len(self.errors) == 1 and self.errors[0].startswith(ErrorMessage.DATASET_NOT_EXISTING.value):
            self.errors.pop()
            return

        self.fail("Only dataset not deleted error expected, instead got: " + str(self.errors))

    def test_delete_database_deleted_dataset(self):
        self.current_dir = os.getcwd()
        connection = self.file_adapter.import_dictionary_from_standard_path("sql_connection.json")
        database = connection["database"]
        user = connection["user"]
        passwort = connection["password"]
        host = connection["host"]
        port = connection["port"]
        self.database_connection = create_engine(f"postgresql://{user}:{passwort}@{host}:{port}/{database}")
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))
        self.controller.communication_facade.import_dataset(["file/data_for_tests/intern_data.csv"],
                                                            "test_data", "intern")
        uuid = self.get_first_event().id
        self.assertEqual(len(self.messages), 1)
        self.messages.pop()

        self.delete_dataset(uuid)

        self._check_dataset_not_existing(uuid=uuid)



class TestOpenDataset(StartedStoppedControllerTest):
    def test_open_dataset(self):
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))
        self.open_dataset_highD(["file/data_for_tests/01_recordingMeta.csv",
                                 "file/data_for_tests/01_tracksMeta.csv",
                                 "file/data_for_tests/01_tracks.csv"])
