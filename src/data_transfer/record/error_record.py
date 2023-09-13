from src.data_transfer.content.error import ErrorMessage


class ErrorRecord:
    def __init__(self, error_type: ErrorMessage, args: str = ""):
        """
        Constructor for a new Error Record
        """
        self._error_type = error_type
        self._args = args

    @property
    def args(self) -> str:
        """
        Returns the string arguments of the error
        """
        return self._args

    @property
    def error_type(self) -> ErrorMessage:
        """
        Returns the error type of the error record
        """
        return self._error_type

