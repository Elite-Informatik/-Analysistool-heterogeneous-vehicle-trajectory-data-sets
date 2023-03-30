from threading import Thread, enumerate

from src.data_transfer.record import ErrorRecord


class ThreadLogger():
    def __init__(self, function):
        self.function = function
        self.thread = None

    def log_thread(self):
        print("Logging: thread execution began: " + str(self.thread) + self.function.__name__)
        running_threads: str = "Logging: Running Threads: "
        for thread in enumerate():
            running_threads += (str(thread) + ", ")
        print(running_threads)
        self.function()

    def start(self) -> Thread:
        thread = Thread(target=self.log_thread)
        self.thread = thread
        thread.start()
        return thread


def logging(func):
    def wrapper(*args, **kwargs):
        objects = args[1:]
        print("Logging: " + func.__name__)
        for object in objects:
            if isinstance(object, ErrorRecord):
                print(object.error_type.value + ": " + object.args)
            else:
                print(str(object))
        return func(*args, **kwargs)

    return wrapper
