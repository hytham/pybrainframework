import unittest 
import numpy as np
from braingraph import braingraph
from nodes.constnode import constnode
from messagedb import messagedb

class braingraph_unittest(unittest.TestCase):
    graph = braingraph()
    def test_add_nodes_agent(self):
        messagedb.Singletone().Clean()                
        self.graph.add(constnode(),"const1")
        self.assertTrue(len(self.graph.nodes)  == 1 )
    def test_get_node_with_name_or_id(self):
        messagedb.Singletone().Clean();         
        self.graph.add(constnode(),"const1")
        node = self.graph.get("const1")
        self.assertTrue(node['Name'] == "const1")
    def test_add_douplicate_throw_execption(self):       
        messagedb.Singletone().Clean();
        self.graph.add(constnode(),"const1")
        self.graph.add(constnode(),"const1")
        self.assertRaises(Exception,'Pre-exisiting node')
    def test_add_two_throw_execption(self):        
        messagedb.Singletone().Clean();
        self.graph.add(constnode(),"const1")
        self.graph.add(constnode(),"const2")
        self.assertTrue(len(self.graph.nodes)  == 2 )
    def test_add_connection_to_node(self):        
        messagedb.Singletone().Clean();
        self.graph.add(constnode(),"const1")
        self.graph.add(constnode(),"const2")
        self.graph.connect("const1","const2")
        self.assertRaises(Exception,'Fail to connect')

    def test_update_node_value(self):        
        messagedb.Singletone().Clean();
        self.graph.add(constnode(),"const1")
        node = self.graph.get("const1")
        self.graph.update_attribute(node,'Value','2')
        node = self.graph.get("const1")
        self.assertEqual('2',node["Value"])

    def test_node_post_payload(self):        
        messagedb.Singletone().Clean();
        self.graph.add(constnode(),"const1")
        self.graph.connect('const1','const1')
        self.graph.post("const1",np.ones(1))
        payload = messagedb.Singletone().Read("const1")
        self.assertEqual(1,payload)


    def test_run_two_connected_node(self):        
        messagedb.Singletone().Clean();
        self.graph.init()
        self.graph.add(constnode(),"const1")
        self.graph.add(constnode(),"const2")        
        self.graph.connect("const1","const2")
        self.graph.post("const1",np.ones(1)*2)
        self.graph.run()
        const2_payload = messagedb.Singletone().Read('const2')
        self.assertEqual(2,const2_payload[0])
    # def test_run_two_connected_node_on_spertae_threads(self):
    #     graph = braingraph()
    #     graph.init()
    #     graph.add(constnode(),"const1")
    #     graph.add(constnode(),"const2")        
    #     graph.connect("const1","const2")
    #     graph.post("const1",np.ones(1)*2)
    #     graph.run(on_new_thread=True)
    #     time.sleep(1) 
    #     graph.stop()
    #     const2_payload = messagedb.Singletone().Read('const2')
    #     self.assertEqual(2,const2_payload[0])

if __name__ == '__main__': 
    unittest.main() 