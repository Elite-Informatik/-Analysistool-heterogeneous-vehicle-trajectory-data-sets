import unittest

from src.controller.output_handling.event import FilterAdded
from src.controller.output_handling.event import FilterComponentDeleted
from src.controller.output_handling.event import RefreshTrajectoryData
from src.data_transfer.content import Column
from src.data_transfer.content import FilterType
from src.data_transfer.content.global_constants import FilterHandlerNames
from src.data_transfer.record import FilterRecord
from src.data_transfer.record import SettingRecord
from test.integration.pseudo_monkey.setting_combination_tester import possible_setting_combination
from test.integration.test_open_fcdui_dataset import OpenFCDUIDatasetControllerTest


class DiscreteFilterTestI(OpenFCDUIDatasetControllerTest):

    def setUp(self) -> None:
        super().setUp()
        filter_types = self.controller.data_request_facade.get_filter_types()
        self.assertTrue(FilterType.DISCRETE.value in filter_types, "Discrete filter not available")
        self.filter_record: FilterRecord = self.controller.data_request_facade.get_filter_selections(
            FilterType.DISCRETE.value)
        self.assertIsNotNone(self.filter_record)
        self.assertIsNotNone(self.filter_record.column)
        self.assertIsNotNone(self.filter_record.discrete)
        self.assertNotEqual(len(self.filter_record.column.selection.option.get_option()), 0,
                            "No columns available in the discrete filter")
        self.point_root_id = self.controller.data_request_facade.get_point_filters_root()
        self.trajectory_root_id = self.controller.data_request_facade.get_trajectory_filters_root()

    def test_filter_combinations(self):
        for column_setting in possible_setting_combination(self.filter_record.column):
            current_selected = column_setting.selection.selected[0]
            discrete_setting = self.controller.data_request_facade.get_discrete_selection_column(current_selected)
            for discrete_setting in possible_setting_combination(discrete_setting):
                with self.subTest(msg="Adding and deleting discrete trajectory filter with combination: "
                                      + str(column_setting.selection.selected)
                                      + " and " + str(discrete_setting.selection.selected)):
                    self.add_delete_filter(column_setting=column_setting, discrete_setting=discrete_setting,
                                           handler=FilterHandlerNames.TRAJECTORY_FILTER_HANDLER)

                with self.subTest(msg="Adding and deleting discrete point filter with combination: "
                                      + str(column_setting.selection.selected)
                                      + " and " + str(discrete_setting.selection.selected)):
                    self.add_delete_filter(column_setting=column_setting, discrete_setting=discrete_setting,
                                           handler=FilterHandlerNames.POINT_FILTER_HANDLER)
        print(self.messages)

    def get_updated_record(self, column_setting: SettingRecord, discrete_setting: SettingRecord,
                           handler: FilterHandlerNames):
        return FilterRecord(_name=self.filter_record.name,
                            _structure_name=handler.value,
                            _enabled=True,
                            _negated=False,
                            _type=self.filter_record.type,
                            _column_setting=column_setting,
                            _discrete_setting=discrete_setting,
                            _interval_setting=None,
                            _polygon_setting=None)

    def add_delete_filter(self, column_setting: SettingRecord, discrete_setting: SettingRecord,
                          handler: FilterHandlerNames):
        self.errors = []
        self.warnings = []
        self.controller.communication_facade.add_filter(
            filter_record=self.get_updated_record(column_setting=column_setting,
                                                  discrete_setting=discrete_setting,
                                                  handler=handler),
            parent_id=self.point_root_id if handler == FilterHandlerNames.POINT_FILTER_HANDLER else self.trajectory_root_id
        )
        self.check_errors([])
        self.check_warnings([])
        self.check_event_types([FilterAdded, RefreshTrajectoryData])
        self.get_first_event()
        filter_id = self.get_first_event().id
        self.assert_no_user_inputs()

        # check if the filter is applied correctly. Only the single filtered trajectories should be shown.
        shown_trajectories = self.controller.data_request_facade.get_shown_trajectories()

        if column_setting.selection.selected[0] == Column.TRAJECTORY_ID:
            self.assertEqual(1, len(shown_trajectories), "Only one trajectory should be shown, when filtering for the"
                                                         "trajectory id. But " + str(len(shown_trajectories))
                             + " are shown.")
            self.assertListEqual(discrete_setting.selection.selected,
                                 [str(self.controller.data_request_facade.get_shown_trajectories()[0].id)])

        self.controller.communication_facade.delete_filter(filter_id)
        self.check_event_types([FilterComponentDeleted, RefreshTrajectoryData])
        self.events.pop()
        self.events.pop()
        self.event_types.pop()
        self.event_types.pop()
        self.assert_no_user_inputs()


if __name__ == '__main__':
    unittest.main()
