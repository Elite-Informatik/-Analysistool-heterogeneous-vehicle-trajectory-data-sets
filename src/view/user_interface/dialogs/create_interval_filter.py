import tkinter as tk
from tkinter.simpledialog import Dialog

from src.data_transfer.record import FilterRecord
from src.view.user_interface.dialogs.filter_creator import FilterCreator
from src.view.user_interface.selection.selection_unit_factory import SelectionUnitFactory


class CreateIntervalFilterDialog(Dialog, FilterCreator):
    """
    Implements a dialog that enables the user to create and edit interval filters.
    """

    def __init__(self, filter_record: FilterRecord, structure_name: str, selection_callback: callable,
                 edit: bool = False):
        """
        Creates a new dialog from an existing filter record. The filter record for a filter that should
        be created from base on is a standard filter defined by the controller.
        The dialog will be immediately displayed on the screen when the constructor is called.
        :param filter_record: the filter that initializes the dialog
        :param selection_callback: callback method to get a selection for the values of a column. The column
                                    needs to be passed as a parameter to the function
        :param edit: indicates if the filter is edited. if not a new filter is created. The title of the window
                    changes depending on the dialog usage (edit or creation)
        """
        self._filter = filter_record

        self._value_selection_callback = selection_callback
        self._structure_name = structure_name
        self._is_valid = False

        self._value_setting_record = filter_record.intervall
        self.column_selection = self._filter.column

        self._interval_frame: tk.Frame = None
        self._name_entry: tk.Entry = None
        self._name_selector = tk.StringVar(value=self._filter.name)

        if edit is True:
            title = "Edit Interval Filter"
        else:
            title = "Create Interval Filter"

        super().__init__(parent=None, title=title)

    def body(self, master):
        """
        builds the body of the dialog
        """
        tk.Label(master=master, text="filter name", anchor="w").grid(column=0, row=0, sticky="nsew")

        self._name_entry = tk.Entry(master=master, textvariable=self._name_selector)
        self._name_entry.grid(column=1, row=0, sticky="nsew")

        self._column_selector = SelectionUnitFactory.create_selection_unit(setting_record=self.column_selection)
        self._view_column_selector = self._column_selector.build(master=master)

        # the event is not processed by the lamda but it is always passed for tkinter bind callbacks
        self._column_selector.add_callback(callback_function=lambda: self._build_value_selection(master=master))
        self._view_column_selector.grid(column=0, row=1, columnspan=2, sticky="nsew")

        self._interval_frame = tk.Frame(master=master)
        self._value_selector = SelectionUnitFactory.create_selection_unit(setting_record=self._value_setting_record)
        self._view_value_selector = self._value_selector.build(master=self._interval_frame)
        self._view_value_selector.grid(column=0, row=0, sticky="nsew")
        self._interval_frame.grid(column=0, row=3, sticky="nsew")

    def _build_value_selection(self, master):
        if self._interval_frame is not None:
            self._interval_frame.destroy()
        self._interval_frame = tk.Frame(master=master)

        new_column_setting = self._column_selector.get_chosen_setting_record()
        column = new_column_setting.selection.selected[0]

        self._value_setting_record = self._value_selection_callback(column)
        self._value_selector = SelectionUnitFactory.create_selection_unit(setting_record=self._value_setting_record)
        self._view_value_selector = self._value_selector.build(master=self._interval_frame)
        self._view_value_selector.grid(column=0, row=0)
        self._interval_frame.grid(column=0, row=3)

    def validate(self) -> bool:
        self._is_valid = self._value_selector.validate() and self._column_selector.validate()
        return self._is_valid

    def apply(self):
        value_settings = self._value_selector.get_chosen_setting_record()
        column_settings = self._column_selector.get_chosen_setting_record()
        self._filter = FilterRecord(
            _name=self._name_selector.get(),
            _negated=False,
            _enabled=True,
            _structure_name=self._structure_name,
            _type=self._filter.type,
            _interval_setting=value_settings,
            _column_setting=column_settings,
            _polygon_setting=None,
            _discrete_setting=None
        )

    def is_valid(self) -> bool:
        return self._is_valid

    def get_new_filter(self) -> FilterRecord:
        return self._filter
