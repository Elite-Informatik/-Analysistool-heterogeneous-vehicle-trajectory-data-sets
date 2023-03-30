import tkinter as tk
from tkinter import ttk
from typing import Dict
from typing import List
from uuid import UUID
from tktooltip import ToolTip

from src.controller.output_handling.event import PolygonAdded
from src.controller.output_handling.event import PolygonChanged
from src.controller.output_handling.event import PolygonDeleted
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler import IEventHandlerSubscribe
from src.view.event_handler.event_consumers.polygon_event_consumer import PolygonEventConsumer
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.ui_util.texts import EnglishTexts


class PolygonSideBar(UiElement, PolygonEventConsumer):
    """
    The Polygon sidebar is used Ui Element that creates a Sidebar in which the user can manage
    the polygons. The class is a PolygonEventConsumer and thereby gets notified by all Polygon events
    and is able to process all Polygon events
    """

    def __init__(self, controller_communication: ControllerCommunication, data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe):
        """
        creates a polygon sidebar instance
        """
        super().__init__(controller_communication, data_request, event_handler)
        self._event_handler = event_handler
        self._event_handler.subscribe_polygon_events(self)

        # maps the polygon id to the tree view entry id
        self._polygon_entries: Dict[UUID, str] = {}
        self._bar: ttk.Treeview = None
        self._clicked_item = None
        self._entry_menu: tk.Menu = None

        self._polygons: List[UUID] = []

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See documentation of the UiElement class.
        """
        self._base_frame = tk.Frame(master=master)
        self._base_frame.columnconfigure(0, weight=1)
        self._base_frame.rowconfigure(0, weight=1)

        self._bar = ttk.Treeview(master=self._base_frame)
        self._bar.heading("#0", text="Polygons")

        for polygon_id in self._polygons:
            polygon_record = self._data_request.get_polygon(polygon_id)
            new_entry = self._bar.insert("", "end", text=polygon_record.__repr__())
            self._polygon_entries[polygon_id] = new_entry
        self._bar.bind("<Button-3>", self.on_right_click)
        self._bar.grid(column=0, row=0, sticky="nsew")

        self._entry_menu = tk.Menu(master=self._base_frame, tearoff=0)
        self._entry_menu.add_command(label="delete", command=self.delete_polygon)

        ToolTip(widget=self._bar, msg=EnglishTexts.POLYGON_BAR_TIP.value, delay=0.5)

        return self._base_frame

    def destroy(self):
        """
        See documentation of the UiElement class.
        """
        if self._bar is not None:
            self._bar.destroy()
        self._bar = None
        self._entry_menu = None
        self._polygon_entries = {}

    def delete_polygon(self):
        """
        This method gets called when the user clicks the delete section in the contextmenu of a polygon entry
        """
        if self._clicked_item is not None and self._bar is not None:
            for key, value in self._polygon_entries.items():
                if value == self._clicked_item:
                    self._controller_communication.delete_polygon(uuid=key)
                    break
        self._clicked_item = None

    def on_right_click(self, event):
        """
        defines what happens on a right click on the polygon sidebar
        """
        self._clicked_item = self._bar.identify_row(event.y)
        # TreeView class indicates no element with an empty string ""
        if not self._clicked_item == "":
            self._entry_menu.tk_popup(event.x_root, event.y_root)

    def process_added_polygon(self, event: PolygonAdded):
        """
        Adds a polygon to the polygon sidebar
        """
        self._polygons.append(event.id)
        if self._bar is not None:
            polygon_record = self._data_request.get_polygon(event.id)
            new_entry = self._bar.insert("", "end", text=polygon_record.__repr__())
            self._polygon_entries[event.id] = new_entry

    def process_deleted_polygon(self, event: PolygonDeleted):
        """
        Deletes a Polygon in the sidebar
        """
        self._polygons.remove(event.id)
        if self._bar is not None:
            polygon_entry = self._polygon_entries[event.id]
            self._bar.delete(polygon_entry)
            del self._polygon_entries[event.id]

    def process_changed_polygon(self, event: PolygonChanged):
        """
        Changes the Polygon data in the Polygon sidebar
        """
        if self._bar is not None:
            polygon_record = self._data_request.get_polygon(event.id)
            polygon_entry = self._polygon_entries[event.id]
            self._bar.item(polygon_entry, text=polygon_record.__repr__())
