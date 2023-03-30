from src.data_transfer.record import PageRecord
from src.data_transfer.record import SegmentRecord
from src.view.user_interface.static_windows.ui_element_factory import UiElementFactory


class SettingsWindowFactory(UiElementFactory):
    """
    This class is a factory for all the ui elements of the settings window.
    It is used to provide the ui elements with the system interfaces.
    The imports are done locally to prevent circular imports.
    """
    def create_base_frame(self):
        """
        Creates a new base frame of the settings window
        """
        from src.view.user_interface.static_windows.settings_window.settings_window_elments.settings_base_frame import \
            SettingsBaseFrame
        return SettingsBaseFrame(data_request=self._data_request,
                                 controller_communication=self._controller_communication,
                                 event_handler=self._event_handler,
                                 factory=self)

    def create_settings_page(self, settings: PageRecord):
        """
        Creates a new settings page
        """
        from src.view.user_interface.static_windows.settings_window.settings_window_elments.settings_page import \
            SettingsPage
        return SettingsPage(self, settings)

    def create_settings_segment(self, settings: SegmentRecord):
        """
        Creates a new settings segment
        """
        from src.view.user_interface.static_windows.settings_window.settings_window_elments.settings_segment import \
            SettingsSegment
        return SettingsSegment(settings, controller_communication=self._controller_communication)
