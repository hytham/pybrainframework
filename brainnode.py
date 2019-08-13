'''
An abstract class that all nodes must drive from
'''
from abc import ABC, abstractmethod
from messagedb import messagedb as mdb
class brainnode(ABC):
    def __init__(self,nodeName):
        self.nodeProparties = {
            "Name": nodeName
        }
    
    @abstractmethod
    def Load(self):
        '''
        Implmented by the child class  
        Load the node in memory
        '''
        pass
    @abstractmethod
    def Run(self,nparray):
        '''
        Excute the node will be called bt the Brain Agent
        this will take a numpy array as an input and must return back an other numpy array
        as an output 
        '''
        pass
    def Set(self,name,value):
        self.nodeProparties[name] = value
    def Get(self,name):
        return self.nodeProparties[name]
       
  
   
   
         