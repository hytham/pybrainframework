import uuid 
from messagedb import messagedb as mdb

class braingraph:
   nodes = []
   def add(self,node):
      '''
      Add a a node to a graph
      '''
      self.nodes.append({
         "Id":self.__getId(),
         "Name":node.nodeProparties["Name"],
         "Node":node
      })
   def connect(self,name):
         '''   
         Add a node with name to list of connections that 
         the graph will post the message to when the run is successful         
         '''
         raise NotImplementedError
   
   def run(self):
         '''
         loop throw all nodes and 
         get any message that is active for that node and 
         invoke run for that node
         then invoke post
         '''
         [__runnode(n) for n in nodes]
   def __runnode(node):
          '''
            This private method will get the message invoke run and post the message back
          '''
          raise NotImplementedError
          
   
     

      
   def __getId(self):
      return uuid.uuid1()