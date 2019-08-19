import unittest

from brainframework import Agent, ExecutionType
from logger import TextLogger, Logger
from nodes.core.Const import Const


class brainagent_unittest(unittest.TestCase):
    def test_create_sequential_graph(self):
        graph = Agent.CreateSequentialGraph()
        self.assertEqual(ExecutionType.sequential, graph.GetExecutionType())

    def test_add_nodes_to_parallel_graph(self):
        logfile = "res/sample.log"
        txt_log = TextLogger(logfile)
        log = Logger(txt_log)

        graph = Agent.CreateThreadedGraph()
        graph.Add(Const(log), "test")
        graph.Add(Const(log), "test2")
        self.assertRaises(Exception, 'Parallel graph must only contain one node')


if __name__ == '__main__':
    unittest.main()
