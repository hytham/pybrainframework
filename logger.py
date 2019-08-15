'''
This class will log any error to an internal stream 
then dump it o text file
'''
from abc import abstractmethod, ABC


class loggerstream(ABC):
    @abstractmethod
    def Write(self, type: object, stream: object) -> object:
        pass


class textlogger(loggerstream):
    def __init__(self, file_path):
        self.log_filepath = file_path

    def Write(self, type, text):
        with open(self.log_filepath, "w+") as f:
            f.write("[%s] %d \r\n", type, text)
            f.close()


class logger:
    def __init__(self, logger_stream):
        assert isinstance(logger_stream, loggerstream)
        self.stream = logger_stream

    def log_i(self, message):
        self.stream.Write("INFO", message)

    def log_d(self, message):
        self.stream.Write("DBG", message)
