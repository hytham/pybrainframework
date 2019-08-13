import unittest
from braingraph import braingraph
from nodes.constnode import constnode

class braingraph_test(unittest.TestCase):
    def test_add_nodes_agent(self):
        graph = braingraph()
        graph.add(constnode())
        self.assertIsNotNone(graph)
    def test_run_two_nodes(self):
        pass

if __name__ == '__main__': 
    unittest.main() 