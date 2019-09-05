import unittest
import numpy as np
from BrainFramework import NodeGraph
from Logger import TextLogger, Logger
from nodes.core.Const import Const
from __messagedb import messagedb


class braingraph_unittest(unittest.TestCase):
    graph = NodeGraph()

    def test_add_nodes_agent(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)

        messagedb.Singletone().Clean()
        self.graph.Add(Const(log), "const1")
        self.assertTrue(len(self.graph.nodes) == 1)

    def test_get_node_with_name_or_id(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        messagedb.Singletone().Clean();
        self.graph.Add(Const(log), "const1")
        node = self.graph.Get("const1")
        self.assertTrue(node['Name'] == "const1")

    def test_add_douplicate_throw_execption(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        messagedb.Singletone().Clean();
        self.graph.Add(Const(log), "const1")
        self.graph.Add(Const(log), "const1")
        self.assertRaises(Exception, 'Pre-exisiting node')

    def test_add_two_throw_execption(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        messagedb.Singletone().Clean();
        self.graph.Add(Const(log), "const1")
        self.graph.Add(Const(log), "const2")
        self.assertTrue(len(self.graph.nodes) == 2)

    def test_add_connection_to_node(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        messagedb.Singletone().Clean();
        self.graph.Add(Const(log), "const1")
        self.graph.Add(Const(log), "const2")
        self.graph.Connect("const1", "const2")
        self.assertRaises(Exception, 'Fail to connect')

    def test_update_node_value(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        messagedb.Singletone().Clean();
        self.graph.Add(Const(log), "const1")
        node = self.graph.Get("const1")
        self.graph.Update(node, 'Value', '2')
        node = self.graph.Get("const1")
        self.assertEqual('2', node["Value"])

    def test_node_post_payload(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        messagedb.Singletone().Clean();
        self.graph.Add(Const(log), "const1")
        self.graph.Connect('const1', 'const1')
        self.graph.Post("const1", np.ones(1))
        payload = messagedb.Singletone().Read("const1")
        self.assertEqual(1, payload)

    def test_run_two_connected_node(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)
        messagedb.Singletone().Clean()

        self.graph.Add(Const(log), "const1")
        self.graph.Add(Const(log), "const2")
        self.graph.Connect("const1", "const2")
        self.graph.Post("const1", np.ones(1) * 2)
        self.graph.Run()
        const2_payload = messagedb.Singletone().Read('const2')
        self.assertEqual(2, const2_payload[0])


if __name__ == '__main__':
    unittest.main()
