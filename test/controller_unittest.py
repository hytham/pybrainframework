from unittest import TestCase

from BrainFramework import controller, NodeGraph
from Logger import TextLogger, Logger
from nodes.core.SinkNode import SinkNode
from nodes.core.Const import Const


class TestController(TestCase):

    def test_createSimpleTesGraph(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)

        const = Const(log)
        sink = SinkNode(log)

        graph = NodeGraph()
        graph.Add(const, "const1")
        graph.Add(sink, "sink1")

        graph.Connect("const1", "sink1")
        control = controller()

        control.Start()

        self.assertEqual(1, 1)

    def test_LoadFromJson(self):
        self.fail()

    def test_LoadSettings(self):
        self.fail()
