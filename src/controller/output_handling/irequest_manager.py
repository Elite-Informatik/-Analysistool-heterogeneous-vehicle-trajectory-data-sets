from abc import ABC
from abc import abstractmethod
from typing import List

from src.data_transfer.record import ErrorRecord
from src.data_transfer.record import SettingRecord


class IRequestManager(ABC):

    @abstractmethod
    def send_warnings(self, warnings: List[str]):
        pass

    @abstractmethod
    def send_errors(self, errors: List[ErrorRecord]):
        pass

    @abstractmethod
    def send_messages(self, messages: List[str]):
        pass

    @abstractmethod
    def request_selection(self, selection: SettingRecord) -> SettingRecord:
        pass

    @abstractmethod
    def ask_acceptance(self, context: str, accept_msg: str) -> bool:
        """
        asks the user for acceptance
        :param message: the message
        :return: true if the user accepted
        """
        pass
