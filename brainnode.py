'''
An abstract class that all nodes must drive from
'''
import numpy as np
from abc import ABC, abstractmethod
from messagedb import messagedb
class brainnode(ABC):
    
    def __init__(self,nodeName):
        self.nodeProparties = {
            "NodeType": nodeName
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
    
    def set(self,name,value):
        self.nodeProparties[name] = value
    def get(self,name):
        return self.nodeProparties[name]

    
       
  
   
   
         