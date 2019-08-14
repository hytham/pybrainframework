import uuid
import numpy as np
import threading
from enum import Enum
from messagedb import messagedb
from multiprocessing import Process

class ExecutionType(Enum):
       sequential = 1
       threaded = 2
       parallal = 3
'''
A brain graph is a collection of nodes that work in sequential manner on a sperate thread 
'''
class braingraph:
   nodes = []
   __is_running =True
   __execution_type = ExecutionType.sequential

   def set_execution_type(self,execution_type):
          self.__execution_type = execution_type
   def get_execution_type(self):
          return self.__execution_type
   def init(self):
      '''
      initalize the graph
      '''
      self.is_init = True
   def add(self,node,name):
      '''
      Add a a node to a graph
      '''
      if(self.node_exist(name)):
           raise Exception('Pre-exisiting node')
      self.nodes.append({
         "Id":self.__getId(),
         "Type":node.nodeProparties["NodeType"],
         "Name":name,
         "Node":node,        
         "Connect":[]
      })
      messagedb.Singletone().Write(np.zeros(1),name)

   def node_exist(self,name):
         '''
         Test to see if a noe with an anme exisit
         '''
         node = [n for n in self.nodes if n['Name'] == name]
         return len(node) > 1
          
   def get(self,name):
      '''
      Get a node with a  specific name
      '''
      node = [n for n in self.nodes if n['Name'] == name]
      if len(node) == 0:
             raise Exception('Node do not exisit')
      return node[0]

   def connect(self,node1,node2):
         '''   
         Add a node with name to list of connections that 
         the graph will post the message to when the run is successful         
         '''
         try:
             [n['Connect'].append(node2) for n in self.nodes if n['Name'] == node1]
         except:
            raise Exception('Fail to connect')
        
   
   def run(self):
         '''
         loop throw all nodes and 
         get any message that is active for that node and 
         invoke run for that node
         then invoke post
         '''
         if not self.is_init:
                raise Exception('Graph must be initaized first befor running')
         if self.get_execution_type() == ExecutionType.sequential:
               [self.__runnode(n) for n in self.nodes]
         elif self.get_execution_type() == ExecutionType.threaded:
               [threading.Thread(target=self.__runnode(n)).start() for n in self.nodes]
         else:
               [Process(target=self.__loop(n)).start() for n in self.nodes]
   def stop(self):
      '''
      Stop all running threads
      '''
      self.__is_running = False

   def __loop(self,node):
          while self.__is_running:
                 self.__runnode(node)
                 
   def __runnode(self,node):
          '''
            This private method will get the message invoke run and post the message back
          '''
          if messagedb.Singletone().IsActive(node['Name']):
               payload = messagedb.Singletone().Read(node['Name'])
               result = node['Node'].Run(payload)
               [ self.post(c,result) for c in node['Connect']]
   def post(self,connection,payload):
         '''
         Post a message to a specific connection
         '''
         messagedb.Singletone().Write(payload,connection)

   def update_value(self,name,newvalue):
          '''
          Update the node value to a new value
          '''
          node = self.get(name)
          self.update_attribute(node,'Value',newvalue)

   def update_attribute(self,node,attribute,newvalue):
          node[attribute] = newvalue

      
   def __getId(self):
      return uuid.uuid1()