import unittest 
import json
from  brainframework import brainagent, ExecutionType
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
    def test_create_graph_from_json(self):
        with open("./test/res/agent.json") as f:
            graph = brainagent.create_fromjson(json.load(f))
        self.assertIsNone(graph)



if __name__ == '__main__': 
    unittest.main()