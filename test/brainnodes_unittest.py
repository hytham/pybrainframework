import unittest
import numpy as np
from nodes.constnode import constnode

class brainnodes_test(unittest.TestCase):
    def test_create_const_node(self):
        node = constnode()
        self.assertEqual("const",node.nodeProparties["NodeType"])

    def test_set_const_node(self):
        node = constnode()
        node.set("Value",1)
        self.assertEqual(1,node.nodeProparties["Value"])
    
    def test_get_const_node(self):
        node = constnode()
        node.set("Value",1)
        self.assertEqual(1,node.get("Value"))

if __name__ == '__main__': 
    unittest.main() 