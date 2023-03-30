import tkinter as tk
from tkinter.simpledialog import Dialog

from src.data_transfer.record import FilterRecord
from src.view.user_interface.dialogs.filter_creator import FilterCreator
from src.view.user_interface.selection.selection_unit_factory import SelectionUnitFactory


class CreatePolygonFilterDialog(Dialog, FilterCreator):
    """
    Implements a dialog that enables the user to create a polygon Filter.
    """

    def __init__(self, filter_record: FilterRecord, structure_name: str, edit: bool = False):
        """
        The dialog will be immediately displayed on the screen when the constructor is called.
        """
        self._name_entry = None
        self._polygon_selector = None
        self._polygon_setting_record = filter_record.polygons
        self._filter = filter_record
        self._structure_name = structure_name
        self._is_valid = False

        self._name_selector = tk.StringVar(value=filter_record.name)

        if edit:
            title = "Edit Polygon Filter"
        else:
            title = "Create Polygon Filter"
        super().__init__(parent=None, title=title)

    def body(self, master):

        tk.Label(master=master, text="filter name", anchor="w").grid(column=0, row=0, sticky="nsew")
        self._name_entry = tk.Entry(master=master, textvariable=self._name_selector)
        self._name_entry.grid(column=1, row=0, sticky="nsew")

        self._polygon_selector = SelectionUnitFactory.create_selection_unit(setting_record=self._polygon_setting_record)
        self._polygon_selector.build(master=master).grid(column=0, row=1, columnspan=2)

    def validate(self) -> bool:

        self._is_valid = self._polygon_selector.validate()
        return self._is_valid

    def apply(self):

        polygon_selection_setting = self._polygon_selector.get_chosen_setting_record()
        self._filter = FilterRecord(
            _name=self._name_selector.get(),
            _enabled=True,
            _negated=False,
            _structure_name=self._structure_name,
            _type=self._filter.type,
            _polygon_setting=polygon_selection_setting,
            _discrete_setting=None,
            _column_setting=None,
            _interval_setting=None)

    def is_valid(self):

        return self._is_valid

    def get_new_filter(self):

        return self._filter
