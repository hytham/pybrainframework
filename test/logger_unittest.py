import unittest

from Logger import TextLogger, Logger


class messagebusdb_test(unittest.TestCase):
    def test_text_logger_test(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        log.log_i("Sample is accepted")

        with open(logfile) as fn:
            lines = fn.readlines()
            for line in lines:
                if "Sample is accepted" in line:
                    found = True
                else:
                    found = False
                self.assertTrue(found)
                break


if __name__ == '__main__':
    unittest.main()
