import tkinter as tk

from src.view.user_interface.ui_util.texts import EnglishTexts


def create_interval_instruction_label(master, range_start: int, range_end: int, interval_start: int,
                                      interval_end: int) -> tk.Label:
    if range_end - range_start <= 1:
        return tk.Label(master=master, text=EnglishTexts.SELECTION_ONE_ENTRY_INSTRUCTION.value
                                            + " " + EnglishTexts.SELECTION_VALUE_RANGE_INSTRUCTION.value.format(
            start=str(interval_start), end=str(interval_end), separator=EnglishTexts.SELECTION_SEPARATOR.value))
    else:
        return tk.Label(master=master, text=EnglishTexts.SELECTION_AMOUNT_RANGE_INSTRUCTION.value.format(
            start=str(range_start),
            end=str(range_end - 1)) + " " + EnglishTexts.SELECTION_VALUE_RANGE_INSTRUCTION.value.format(
            start=str(interval_start), end=str(interval_end), separator=EnglishTexts.SELECTION_SEPARATOR.value))


def create_discrete_instruction_label(master, range_start: int, range_end: int) -> tk.Label:
    if range_end - range_start <= 1:
        return tk.Label(master=master, text=EnglishTexts.SELECTION_ONE_ENTRY_INSTRUCTION.value)
    else:
        return tk.Label(master=master, text=EnglishTexts.SELECTION_AMOUNT_RANGE_INSTRUCTION.value.format(
            start=str(range_start), end=str(range_end - 1)))
