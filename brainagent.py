'''
This is the main library that will constratc the brain graphs and mange its execution
'''
from enum import Enum
from braingraph import braingraph,ExecutionType
class brainagent:

    @staticmethod
    def create_sequential_graph():
        graph = braingraph()
        graph.set_execution_type(ExecutionType.sequential)
        return graph
    @staticmethod
    def create_threaded_graph():
        graph = braingraph()
        graph.set_execution_type(ExecutionType.threaded)
        return graph
    @staticmethod
    def create_parallal_graph():
        graph = braingraph()
        graph.set_execution_type(ExecutionType.threaded)
        return graph
    
   
    @staticmethod
    def create_fromjson(self,json):
        '''
        Create an agent froma json file
        '''
        raise NotImplementedError
