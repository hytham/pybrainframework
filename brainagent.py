'''
This is the main library that will constratc the brain graphs and mange its execution
'''

from braingraph import braingraph,ExecutionType
class brainagent:

    @staticmethod
    def create_sequential_graph():
        graph = braingraph()
        graph.get_execution_type(ExecutionType.sequential)
        return graph
    
    def add_nodes(self,nodes=[]):
        '''
        Add Nodes
        '''
        raise NotImplementedError
    @staticmethod
    def create_fromjson(self,json):
        '''
        Create an agent froma json file
        '''
        raise NotImplementedError
