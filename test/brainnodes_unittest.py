import unittest
import numpy as np

from logger import TextLogger, Logger
from nodes.core.Const import Const


class brainnodes_test(unittest.TestCase):
    def test_create_const_node(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        node = Const(log)
        self.assertEqual("const", node.Properties["NodeType"])

    def test_set_const_node(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        node = Const(log)
        node.set("Value", 1)
        self.assertEqual(1, node.Properties["Value"])

    def test_get_const_node(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        node = Const(log)
        node.set("Value", 1)
        self.assertEqual(1, node.Get("Value"))


if __name__ == '__main__':
    unittest.main()
