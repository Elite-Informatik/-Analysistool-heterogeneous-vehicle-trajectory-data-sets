import tkinter as tk
from typing import List

from src.data_transfer.record import PageRecord
from src.view.user_interface.static_windows.settings_window.settings_window_elments.settings_segment import \
    SettingsSegment
from src.view.user_interface.static_windows.settings_window.settings_window_factory import SettingsWindowFactory


class SettingsPage:
    """
    Represents a Page in the settings. Acts like a UiElement with the build and destroy method.
    It does not inherit from UiElement because the pages are created dynamically and dont need be notified about
    any events.
    """

    def __init__(self, factory: SettingsWindowFactory, settings: PageRecord):
        self._factory = factory
        self._record_segments = settings.segment_records
        self._page: PageRecord = settings

        self._base_frame: tk.Frame = None
        self._view_segments: List[SettingsSegment] = []

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See documentation of the UiElement class.
        """
        self._base_frame = tk.Frame(master=master)

        for i, segment in enumerate(self._record_segments):
            view_segment_unbuild = self._factory.create_settings_segment(segment)
            self._view_segments.append(view_segment_unbuild)

            view_segment = view_segment_unbuild.build(master=self._base_frame)
            view_segment.grid(column=0, row=2 * i, sticky="new")
            tk.Frame(master=self._base_frame, width=100, height=2, bg="grey").grid(column=0, row=2 * i + 1,
                                                                                   sticky="nsew")
        return self._base_frame

    def destroy(self):
        """
        See documentation of the UiElement class.
        """
        for segment in self._view_segments:
            segment.destroy()
        self._view_segments = []

    def to_page(self) -> PageRecord:
        """
        Converts the view to a page record.
        :return: The page record with the input values.
        """
        new_segments = []
        segment: SettingsSegment
        for segment in self._view_segments:
            new_segments.append(segment.to_segment())
        return PageRecord(_name=self._page.name, _identifier=self._page.identifier, _segments=tuple(new_segments))

    def validate(self) -> bool:
        """
        Validates the input of the page.
        """
        for segment in self._view_segments:
            if not segment.validate():
                return False
        return True
