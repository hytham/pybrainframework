import time;
from abc import abstractmethod, ABC


class LoggerStream(ABC):
    """
        This class will log any error to an internal stream
        then dump it o text file

    """

    @abstractmethod
    def Write(self, type: object, stream: object) -> object:
        pass


class TextLogger(LoggerStream):
    def __init__(self, file_path):
        self.log_filepath = file_path

    def Write(self, type, text):
        ts = time.time()
        with open(self.log_filepath, "w+") as f:
            f.write("[" + type + "] " + " : " + str(ts) + " : " + text + " \r\n")
            f.close()


class Logger:

    def __init__(self, logger_stream):
        assert isinstance(logger_stream, LoggerStream)
        self.stream = logger_stream

    def log_i(self, message):
        self.stream.Write("INFO", message)

    def log_d(self, message):
        self.stream.Write("DBG", message)

    def log_e(self, exception):
        pass
        # assert.isinstance(Exception,exception)
        # self.stream.Write('[ERR]',exception)
