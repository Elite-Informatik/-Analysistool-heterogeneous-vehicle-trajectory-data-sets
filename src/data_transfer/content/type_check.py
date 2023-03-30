from uuid import UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.controller.execution_handling.abstract_manager import AbstractManager
    from src.model.error_handler import ErrorHandler
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import InvalidInput
from src.data_transfer.exception import InvalidUUID


def type_check(*types: type, error_message: str = "Wrong parameter type for parameter {i} {type} "
                                                  "from function {func} given {given}. "):
    def decorator(func):
        def wrapper(*args, **kwargs):
            controll_args = args[1:]

            for i, arg in enumerate(controll_args):

                if not isinstance(arg, types[i]):
                    # manager = args[0]
                    # if issubclass(manager.__class__, AbstractManager):
                    #    error_handler = ErrorHandler()
                    #    error_handler.throw_error(
                    #        ErrorMessage.INVALID_TYPE,
                    #        error_message.format(i=i, func=func.__name__,type=types[i], given=type(arg))
                    #    )
                    #    manager.handle_error(
                    #        error_origins=[error_handler],
                    #        meta_info="This Error was thrown by the type_check decorator."
                    #    )

                    if types[i] == UUID:
                        raise InvalidUUID(error_message.format(i=i, func=func.__name__,
                                                               type=types[i], given=type(arg)))

                    else:
                        raise InvalidInput(
                            error_message.format(i=i, func=func.__name__, type=types[i], given=type(arg)))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def type_check_assert(*types, error_message: str = "Wrong parameter type for parameter {i} {type} "
                                                   "from function {func} given {given}."):
    def decorator(func):
        def wrapper(*args, **kwargs):
            controll_args = args[1:]
            for i, arg in enumerate(controll_args):
                assert isinstance(arg, types[i]), error_message.format(i=i, func=func.__name__,
                                                                       type=types[i], given=type(arg))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def list_empty_check(*types, error_message: str = "Wrong content type for list {i} from fuction {func}."):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for object in types:
                if not isinstance(object, list):
                    continue
                if len(object) == 0:
                    raise InvalidInput(error_message.format(i=types.index(object), func=func.__name__))
            return func(*args, **kwargs)

        return wrapper

    return decorator
