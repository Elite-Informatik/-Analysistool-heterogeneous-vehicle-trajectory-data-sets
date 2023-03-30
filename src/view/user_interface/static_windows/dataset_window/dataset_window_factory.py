from src.view.user_interface.static_windows.ui_element_factory import UiElementFactory


class DatasetWindowFactory(UiElementFactory):
    """
    Factory that creates the DatasetWindow Elements and provides the Elements
    with the system interfaces. Local imports in the creation function
    to prevent circular imports.
    """

    def create_dataset_base_frame(self):
        """
        Creates a new BaseFrame for the dataset window.
        The BaseFrame is the only UiElement of the dataset window so far.
        """
        from src.view.user_interface.static_windows.dataset_window. \
            dataset_window_elements.dataset_base_frame import DatasetBaseFrame
        return DatasetBaseFrame(controller_communication=self._controller_communication,
                                data_request=self._data_request,
                                event_handler=self._event_handler)
