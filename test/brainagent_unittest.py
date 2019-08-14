import unittest 
from brainagent import brainagent, ExecutionType
from nodes.constnode import constnode

class brainagent_unittest(unittest.TestCase):
    def test_create_sequential_graph(self):
        graph = brainagent.create_sequential_graph()
        self.assertEqual(ExecutionType.sequential , graph.get_execution_type())
    def test_add_nodes_to_parallal_graph(self):
        
         graph = brainagent.create_sequential_graph()
         graph.add(constnode(),"test")
         graph.add(constnode(),"test2")
         self.assertRaises(Exception,'Parallal graph must only contain one node')


if __name__ == '__main__': 
    unittest.main()