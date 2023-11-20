import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from typing import Dict
from typing import List
from uuid import UUID

from src.controller.output_handling.event import DatasetAdded
from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import DatasetOpened
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler import IEventHandlerSubscribe
from src.view.event_handler.event_consumers import DatasetEventConsumer
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.ui_util.texts import EnglishTexts


class DatasetBaseFrame(UiElement, DatasetEventConsumer):
    """
    UiElement that is used to display the datasets and gives the user the possibility to delete datasets.
    The Class implements the DatasetEventConsumer interface because it has to process dataset related
    events.
    """

    def __init__(self, controller_communication: ControllerCommunication, data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe):
        super().__init__(controller_communication, data_request, event_handler)

        self.event_handler = event_handler
        self.event_handler.subscribe_dataset_events(self)

        self._right_click_menu: tk.Menu = None
        # caches the clicked tree item that was clicked
        self._clicked_item = None

        # maps dataset id to row id in the TreeView
        # destroyed and reinitialized with every destruction and build of the window
        self._id_entry_mapping: Dict[UUID, str] = {}
        self._datasets_tree: ttk.Treeview = None

        # stores the datasets during the entire runtime of the application
        self._datasets: List[UUID] = []

    def build(self, master: tk.Widget) -> tk.Widget:
        self._base_frame = tk.Frame(master=master)
        self._base_frame.columnconfigure(0, weight=1)
        self._base_frame.rowconfigure(0, weight=1)

        self._datasets_tree = ttk.Treeview(master=self._base_frame)
        self._datasets_tree["columns"] = ["size"]
        self._datasets_tree.heading("#0", text="name")
        self._datasets_tree.heading("size", text="size")

        for dataset_id in self._datasets:
            meta_data = self._data_request.get_dataset_meta(dataset_id)
            new_entry = self._datasets_tree.insert("", "end", text=meta_data.name, values=[f"{meta_data.size} Bytes"])
            self._id_entry_mapping[dataset_id] = new_entry

        self._right_click_menu = tk.Menu(master=self._base_frame, tearoff=0)
        self._right_click_menu.add_command(label="delete", command=self.delete_dataset)
        self._datasets_tree.bind("<Button-3>", self.on_right_click)
        # button 2 is required for mac-os
        self._datasets_tree.bind("<Button-2>", self.on_right_click)

        self._datasets_tree.grid(column=0, row=0, sticky="nsew")
        return self._base_frame

    def destroy(self):
        """
        Destructs the tree and destroys the base frame.
        Dataset Tree has to be set to None for proper event handling in other methods.
        If Tree is set to none, other methods see that the window is currently not displayed.
        """
        self._id_entry_mapping.clear()
        self._base_frame.destroy()
        self._datasets_tree = None

    def process_added_dataset(self, event: DatasetAdded):
        """
        Adds a new dataset to the displayed datasets.
        If the dataset Tree is None the frame is not build currently so the view
        does not have to be refreshed and will be refreshed automatically with the next build.
        """
        self._datasets.append(event.id)
        if self._datasets_tree is not None:
            meta_data = self._data_request.get_dataset_meta(event.id)
            new_entry = self._datasets_tree.insert("", "end", text=meta_data.name, values=[meta_data.size])
            self._id_entry_mapping[event.id] = new_entry

    def process_deleted_dataset(self, event: DatasetDeleted):
        """
        Deletes a dataset.
        If the dataset Tree is None the frame is not build currently so the view
        does not have to be refreshed and will be refreshed automatically with the next build.
        """
        self._datasets.remove(event.id)
        if self._datasets_tree is not None:
            entry = self._id_entry_mapping[event.id]
            self._datasets_tree.delete(entry)
            del self._id_entry_mapping[event.id]

    def process_opened_dataset(self, event: DatasetOpened):
        """
        The dataset window does not need to process the open dataset event.
        To fulfill the DatasetEventConsumer interface the method is still declared.
        If the method is called by the distributor nothing happens.
        DO NOT REMOVE METHOD!!!
        OTHERWISE, AN ERROR WILL OCCOUR WHEN THE DatasetOpened EVENT GETS DISTRIBUTED.
        """
        pass

    def on_right_click(self, event):
        """
        caches the clicked item and opens the dataset context menu if an item in the tree view was clicked
        """
        self._clicked_item = self._datasets_tree.identify_row(event.y)
        # TreeView class indicates no element with an empty string ""
        if not self._clicked_item == "":
            self._right_click_menu.tk_popup(event.x_root, event.y_root)

    def delete_dataset(self):
        """
        method that gets called to py the context menu entry on click.
        It uses the previous cached clicked item to indicate the dataset that
        should be deleted.
        """
        if self._clicked_item is not None:
            for dataset_id, entry_id in self._id_entry_mapping.items():
                if entry_id == self._clicked_item:
                    name = self._datasets_tree.item(entry_id)['text']
                    result = askyesno(message=EnglishTexts.DATASET_DELETE_SURE.value + f"\n{name}")
                    if result is True:
                        self._controller_communication.delete_dataset(dataset_id)
                    break
        self._clicked_item = None
