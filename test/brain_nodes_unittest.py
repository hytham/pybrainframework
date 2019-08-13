import unittest
from  nodes.constnode import constnode

class brain_nodes_test(unittest.TestCase):
    def test_create_const_node(self):
        node = constnode()
        self.assertEqual("const",node.nodeProparties["Name"])

    def test_set_const_node(self):
        node = constnode()
        node.Set("Value",1)
        self.assertEqual(1,node.nodeProparties["Value"])
    
    def test_get_const_node(self):
        node = constnode()
        node.Set("Value",1)
        self.assertEqual(1,node.Get("Value"))

if __name__ == '__main__': 
    unittest.main() 