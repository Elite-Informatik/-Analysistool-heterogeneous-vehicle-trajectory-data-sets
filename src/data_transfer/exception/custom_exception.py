from enum import Enum


class ModelException(Exception):
    """Raised if an error occurs in the model structure"""

    def __init__(self, message: str):
        self._message = message

    @property
    def message(self) -> str:
        """
        Returns the message of the exception
        """
        return self._message


class InvalidInput(ModelException):
    """Raised if the given input does not match the models expectations"""


class InvalidUUID(ModelException):
    """Raised if the given uuid is not available in the model layer"""


class ObjectInUse(ModelException):
    """Raised if the object modified is used in another component"""


class ExecutionFlowError(ModelException):
    """Raised if a method is getting called that does not fit in the prior execution history"""


class UnexpectedArgumentError(ModelException):
    """Raised if an unexpected argument is passed to a method in the model"""


class IllegalAnalysisError(ModelException):
    """Raised if an illegal Analysis constructor is attempted to be added to the AnalysisStructure"""

    def __init__(self, message: str):
        super().__init__(message)


class StandardPathNotExisting(ModelException):
    """Raised if the standard path is not existing in file system"""


class DictionaryCorrupted(ModelException):
    """Raised if a dictionary does not match the programs expectations"""


class ExceptionMessages(Enum):
    """
    Enum class for all the exception messages
    """
    UNEXPECTED_TYPE = "The parameter of type {passed_type} was passed but not expected. " \
                      "Expected type: {expected_type}, additional information: {additional_info}"
    UNEXPECTED_VALUE = "The parameter of value {passed_value} was passed but not expected. " \
                       "Expected value: {expected_value}, additional information: {additional_info}"
