from typing import List

from src.data_transfer.content.type_check import type_check

from src.controller.facade_consumer.user_input_facade_consumer import UserInputRequestFacadeConsumer
from src.controller.output_handling.irequest_manager import IRequestManager
from src.data_transfer.content.logger import logging
from src.data_transfer.record import ErrorRecord
from src.data_transfer.record import SettingRecord


class InputRequestManager(UserInputRequestFacadeConsumer, IRequestManager):
    """
    represents a manager for the input requests sent to the view
    """

    @logging
    def send_warnings(self, warnings: List[str]):
        """
        sends the given warnings to the view
        :param warnings: the warnings
        """
        for warning in warnings:
            self.user_input_request_facade.send_warning(warning)

    @logging
    def send_errors(self, errors: List[ErrorRecord]):
        """
        Sends given error records to the view
        """
        for error in errors:
            if error.args is not None:
                if len(error.args) > 0:
                    self.user_input_request_facade.send_error(error.error_type.value + " " + error.args)
                    continue
            self.user_input_request_facade.send_error(error.error_type.value)

    def send_exception(self, exception: Exception, meta_info: str):
        """
        Sends given exception to the view
        """
        if len(meta_info) > 0:
            meta_info = " " + meta_info
        self.user_input_request_facade.send_error("An exception was thrown in the execution: "
                                                  + str(exception) + meta_info)

    @logging
    def send_messages(self, messages: List[str]) -> None:
        """
        sends the given messages to the view
        :param messages: the messages
        """
        for message in messages:
            self.user_input_request_facade.send_message(message)

    @logging
    @type_check(SettingRecord)
    def request_selection(self, selection: SettingRecord) -> SettingRecord:
        """
        sends a request in form of a selection record to the user
        :param selection: the selection record
        """
        return self.user_input_request_facade.request_user_input(selection)

    @logging
    @type_check(str, str)
    def ask_acceptance(self, context: str, accept_msg: str) -> bool:
        """
        asks the user for acceptance
        :param message: the message
        :return: true if the user accepted
        """
        return self.user_input_request_facade.ask_acceptance(context, accept_msg)

