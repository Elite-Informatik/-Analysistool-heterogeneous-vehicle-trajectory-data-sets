import tkinter as tk
from tkinter.simpledialog import Dialog

from src.data_transfer.content.logical_operator import LOGICAL_OPERATORS_STRING
from src.data_transfer.record import FilterGroupRecord
from src.view.user_interface.dialogs.filter_group_creator import FilterGroupCreator
from src.view.user_interface.ui_util.texts import EnglishTexts


class CreateFilterGroupDialog(Dialog, FilterGroupCreator):
    """
    Defines a Dialog that is opened when the user wants to create or edit a filter group.
    """

    def __init__(self, filter_group_record: FilterGroupRecord, structure_name: str, edit: bool = False):
        """
        Creates and runs a new create filter group dialog.
        The dialog will be immediately displayed on the screen when the constructor is called.
        :param filter_group_record: contains the initial data of the filter group. If a filter group is changed,
            this record represents the data of the filter group that the user wants to change.
            If the user creates a new filter the record contains the data for a standard filter group.
        :param structure_name: the name of the filter structure in which the filter will be added.
        :param edit: True if the dialog is used to edit an existing filter. False if the dialog is used to create
            a new filter.
        """
        self._name_var = None
        self._enter_name_label = None
        self._name_entry = None
        self._negated_var = None
        self._negate_label = None
        self._negate_box = None
        self._logical_operator_label = None
        self._logical_operator_var = None
        self._logical_operator_selection = None
        self._is_valid: bool = False

        self._filter_group = filter_group_record
        self._structure_name = structure_name

        if edit is True:
            title = EnglishTexts.EDIT_FILTER_GROUP_DIALOG_NAME.value
        else:
            title = EnglishTexts.CREATE_FILTER_GROUP_DIALOG_NAME.value

        super().__init__(parent=None, title=title)

    def body(self, master):
        """
        Defines how the body of the dialog should look like.
        Is a Template method that gets called in the constructor of the super class.
        """
        self._name_var = tk.StringVar()
        self._name_var.set(self._filter_group.name)

        self._enter_name_label = tk.Label(master=master, text="filter group name", anchor="w", width=20).grid(row=0, column=0, sticky="nsew")
        self._name_entry = tk.Entry(master=master, textvariable=self._name_var)
        self._name_entry.grid(row=0, column=1, sticky="nsew")

        self._negated_var = tk.BooleanVar()
        self._negated_var.set(value=self._filter_group.negated)

        self._negate_label = tk.Label(master=master, text="negate filter group", anchor="w", width=20)
        self._negate_label.grid(row=1, column=0, sticky="nsew")

        self._negate_box = tk.Checkbutton(master=master, variable=self._negated_var)
        self._negate_box.grid(row=1, column=1, sticky="w")

        self._logical_operator_label = tk.Label(master=master, text="logical operator", anchor="w", width=20)
        self._logical_operator_label.grid(row=2, column=0, sticky="nsew")

        self._logical_operator_var = tk.StringVar()
        self._logical_operator_var.set(self._filter_group.operator)

        self._logical_operator_selection = tk.OptionMenu(master, self._logical_operator_var, *LOGICAL_OPERATORS_STRING)
        self._logical_operator_selection.grid(row=2, column=1, sticky="w")

    def validate(self) -> bool:
        """
        Proofs if the user input is valid. Since the input for this dialog is always valid.
        The method returns True. It is also a template method that gets called when the ok button
        handler of the super class.
        """
        self._is_valid = True
        return True

    def apply(self):
        """
        Sets the dialog attributes to the corresponding user input values.
        Is also a template method that gets called in the ok button handler of the
        super class but only if the user input is valid.
        """
        self._filter_group = FilterGroupRecord(_name=self._name_var.get(),
                                               _filter_records=self._filter_group.filter_records,
                                               _operator=self._logical_operator_var.get(),
                                               _enabled=True,
                                               _negated=self._negated_var.get(),
                                               _structure_name=self._structure_name)

    def is_valid(self):
        """
        used to proof if the user input was valid after the dialog is closed.
        """
        return self._is_valid

    def get_new_filter_group(self) -> FilterGroupRecord:
        return self._filter_group
