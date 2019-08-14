'''
This is a simple node that will post a const number once

'''
from brainnode import brainnode
class constnode(brainnode):
    def __init__(self):
        return super().__init__("const")
    def Load(self):
        super().Load()
    def Run(self,nparray):        
        return nparray