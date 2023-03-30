import tkinter as tk
from tkinter.simpledialog import Dialog

from src.data_transfer.record import FilterRecord
from src.view.user_interface.dialogs.filter_creator import FilterCreator
from src.view.user_interface.selection.selection_unit_factory import SelectionUnitFactory
from src.view.user_interface.ui_util.texts import EnglishTexts


class CreateDiscreteFilterDialog(Dialog, FilterCreator):
    """
    Implements a Dialog that can be used to create and Edit a discrete Filter
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

        self._name_selector = None
        self._name_entry = None
        self._column_selector = None
        self._view_column_selector = None
        self._is_valid = None
        self._filter = filter_record
        self._structure_name = structure_name

        self._value_setting_record = filter_record.discrete
        self._column_setting_record = filter_record.column

        self._value_selection_callback = selection_callback

        self._view_value_selector = None

        if edit is True:
            title = EnglishTexts.EDIT_DISCRETE_FILTER_DIALOG_NAME.value
        else:
            title = EnglishTexts.CREATE_DISCRETE_FILTER_DIALOG_NAME.value

        super().__init__(parent=None, title=title)

    def body(self, master):
        """
        builds the body of the selection
        """
        self._name_selector = tk.StringVar()
        self._name_selector.set(self._filter.name)

        tk.Label(master=master, text="filter name", anchor="w").grid(column=0, row=0, sticky="nsew")
        self._name_entry = tk.Entry(master=master, textvariable=self._name_selector)
        self._name_entry.grid(column=1, row=0)

        self._column_selector = SelectionUnitFactory.create_selection_unit(setting_record=self._column_setting_record)
        self._view_column_selector = self._column_selector.build(master=master)

        # the event is not processed by the lamda but it is always passed for tkinter bind callbacks
        self._column_selector.add_callback(callback_function=lambda: self._build_value_selection(master=master))
        self._view_column_selector.grid(column=0, row=1, columnspan=2)

        self._value_selector = SelectionUnitFactory.create_selection_unit(setting_record=self._value_setting_record)
        self._view_value_selector = self._value_selector.build(master=master)
        self._view_value_selector.grid(column=0, row=2, columnspan=2)

    def _build_value_selection(self, master):
        """
        Resets the value selection if the column has changed.
        The selection represents all selectable values from the column.
        """
        if self._view_value_selector is not None:
            self._view_value_selector.destroy()
        new_column_setting = self._column_selector.get_chosen_setting_record()
        column = new_column_setting.selection.selected[0]

        self._value_setting_record = self._value_selection_callback(column)
        self._value_selector = SelectionUnitFactory.create_selection_unit(setting_record=self._value_setting_record)
        self._view_value_selector = self._value_selector.build(master=master)
        self._view_value_selector.grid(column=0, row=3)

    def validate(self) -> bool:
        """
        Proofs if the current input is valid. The method is used in a template method in
        the parent class for the ok-Button handler
        """
        if self._column_selector.validate() and self._value_selector.validate():
            self._is_valid = True
        else:
            self._is_valid = False
        return self._is_valid

    def apply(self):
        """
        Sets the new Filter Record based on the user input
        """
        new_value_setting = self._value_selector.get_chosen_setting_record()
        new_column_setting = self._column_selector.get_chosen_setting_record()
        self._filter = FilterRecord(
            _name=self._name_selector.get(),
            _structure_name=self._structure_name,
            _negated=False,
            _enabled=True,
            _type=self._filter.type,
            _column_setting=new_column_setting,
            _discrete_setting=new_value_setting,
            _polygon_setting=None,
            _interval_setting=None
        )

    def is_valid(self) -> bool:
        return self._is_valid

    def get_new_filter(self) -> FilterRecord:
        return self._filter
