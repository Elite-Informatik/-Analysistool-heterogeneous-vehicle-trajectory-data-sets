from src.data_transfer.record import PageRecord
from src.data_transfer.record import SegmentRecord
from src.data_transfer.record import SettingRecord
from src.data_transfer.record import SettingsRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.selection.bool_discrete_option import BoolDiscreteOption
from src.data_transfer.selection.string_option import StringOption
from src.view.user_interface.static_windows.settings_window.settings_window import SettingsWindow
from src.view.user_interface.static_windows.settings_window.settings_window_factory import SettingsWindowFactory


class EventStub:

    def subscribe_settings_events(self, subscribor):
        pass


class ControllerStub:

    def change_settings(self, settings):
        pass


class DataRequestStub:

    def get_settings(self) -> SettingsRecord:
        selection_record1 = SelectionRecord(["aaa"], StringOption("a*"), range(3))
        selection_record2 = SelectionRecord([True], BoolDiscreteOption())
        setting_record1 = SettingRecord("setting_context", selection_record1, "setting_id")
        setting_record2 = SettingRecord("setting_context", selection_record2, "setting_id")

        segment_record = SegmentRecord((setting_record1, setting_record2), "segment_name", "segment_id")
        page_record = PageRecord((segment_record,), "page_name", "page_id")
        return SettingsRecord((page_record,))


def settings_window_test():
    event_stub = EventStub()
    controller_stub = ControllerStub()
    data_request_stub = DataRequestStub()

    settings_window_factory = SettingsWindowFactory(event_stub, controller_stub, data_request_stub)
    SettingsWindow(settings_window_factory).run()


if __name__ == "__main__":
    settings_window_test()
