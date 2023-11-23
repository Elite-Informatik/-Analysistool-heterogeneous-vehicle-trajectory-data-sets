import os
from uuid import uuid4

from src.data_transfer.exception import InvalidInput
from src.data_transfer.exception import InvalidUUID
from test.controller.test_command import OpenInternDatasetControllerTest


class DataRequestTest(OpenInternDatasetControllerTest):
    def setUp(self):
        super().setUp()
        self.call_no_parameter_list = [
            self.controller.data_request_facade.get_filter_types,
            self.controller.data_request_facade.get_filter_group_selection,
            self.controller.data_request_facade.get_trajectory_filters_root,
            self.controller.data_request_facade.get_point_filters_root,
            self.controller.data_request_facade.get_polygon_ids,
            self.controller.data_request_facade.get_analysis_types,
            self.controller.data_request_facade.get_settings,
            self.controller.data_request_facade.get_discrete_filterable_columns,
            self.controller.data_request_facade.get_interval_filterable_columns,
            self.controller.data_request_facade.get_convertable_file_formats,
        ]

        self.call_one_parameter_list = [
            self.controller.data_request_facade.get_rawdata,
            self.controller.data_request_facade.get_filter_selections,
        ]

        self.call_one_uuid_list = [
            #(self.controller.data_request_facade.get_rawdata_trajectory, "get_rawdata_trajectory"),
            (self.controller.data_request_facade.get_polygon, "get_polygon"),
            (self.controller.data_request_facade.get_filter, "get_filter"),
            (self.controller.data_request_facade.get_filter_group, "get_filter_group"),
            #(self.controller.data_request_facade.get_dataset_meta, "get_dataset_meta"),
            (self.controller.data_request_facade.get_analysis_settings, "get_filter_group"),
            (self.controller.data_request_facade.get_analysis_data, "get_analysis_data"),

        ]

    def test_filter_data_request(self):
        filter_types = self.controller.data_request_facade.get_filter_types()
        self.assertIsNotNone(filter_types)
        for filter_type in filter_types:
            self.assertIsNotNone(self.controller.data_request_facade.get_filter_selections(filter_type))
        filter_group_type = self.controller.data_request_facade.get_filter_group_selection()
        self.assertIsNotNone(filter_group_type)

    def test_call_no_parameter(self):
        for call in self.call_no_parameter_list:
            self.assertIsNotNone(call(), f"Mehtod {call} returned unexpected None value.")

    def test_invalid_uuid(self):
        for call, s in self.call_one_uuid_list:
            with self.assertRaises(InvalidUUID):
                call(None)
            with self.assertRaises(InvalidUUID, msg=f"Invalid UUID was not detected for {s}."):
                call(uuid4())

    def test_none_vaues(self):
        for call in self.call_one_parameter_list:
            with self.assertRaises(InvalidInput):
                call(None)

    def test_get_shown_tajecotrys(self):
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))

        self.assertIsNotNone(self.controller.data_request_facade.get_shown_trajectories())
