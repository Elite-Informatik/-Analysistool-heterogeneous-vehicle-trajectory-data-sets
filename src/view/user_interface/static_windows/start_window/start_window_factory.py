from src.view.user_interface.static_windows.ui_element_factory import UiElementFactory


class StartWindowFactory(UiElementFactory):
    """
    This factory creates the Ui-Elements that can be used for the start window.
    Imports are done locally to prevent circular imports.
    """

    def create_start_window_base_frame(self):
        """
        Creates a new base frame of the start window
        """
        from src.view.user_interface.static_windows.start_window.start_window_elements.start_window_base_frame import \
            StartWindowBaseFrame
        return StartWindowBaseFrame(controller_communication=self._controller_communication,
                                    data_request=self._data_request,
                                    event_handler=self._event_handler)
