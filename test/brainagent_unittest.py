import unittest 
from brainagent import brainagent, ExecutionType

class brainagent_unittest(unittest.TestCase):
    def test_create_sequential_graph(self):
        graph = brainagent.create_sequential_graph()
        self.assertEqual(ExecutionType.sequential , graph.get_execution_type())

if __name__ == '__main__': 
    unittest.main()