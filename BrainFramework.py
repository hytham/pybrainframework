import uuid
import numpy as np
import threading
from enum import Enum
from multiprocessing import Process
from abc import ABC, abstractmethod
from __messagedb import messagedb


class controller:
    """
    Is the main agent controller that will setup the brain agent, load any configurations, initialize it,
    start it and manage its life cycle
    """
    full_package_nodes = dict()

    def __init__(self):
        """ Load all modules in a dictionary to be easly constrauct whena json file is read """

        self.seqGraph = Agent.CreateSequentialGraph()
        self.thredGraph = Agent.CreateThreadedGraph()
        self.ProcGraph = Agent.CreateParallelGraph()

    def getAllGraphs(self):
        """ Return all graphs that was created by controller so the main application can use it to add nodes to it"""
        return self.seqGraph, self.thredGraph, self.ProcGraph

    def Start(self):
        self.seqGraph.Run()
        self.thredGraph.Run()
        self.ProcGraph.Run()

    def LoadFromJson(self, json_file_path):
        """ Construct the full graph from json file"""
        seq, thr, proc = self.getAllGraphs()

    def LoadSettings(self, setting_file_path):
        """ Load all teh settings from teh file path"""
        pass


class BrainNode(ABC):
    """
        The base class that all nodes must drive from
        this is the smallest working unit that the agent will execute
    """

    def __init__(self, node_name, logger):
        """
            :node_name: The name of the node
            :type logger: a list of loggers that will be called to log any error
        """
        self.Properties = {
            "NodeType": node_name,
            "Loggers": logger
        }

    @abstractmethod
    def Load(self):
        """
            Implemented by the child class
            Load the node in memory
        """
        pass

    @abstractmethod
    def Run(self, np_array):
        """
            Execute the node will be called bt the Brain Agent
            this will take a numpy array as an input and must return back an other numpy array
            as an output
        """
        pass

    @abstractmethod
    def GetAllowedExecutionType(self):
        """
            Must return a list of all the execution type this node is allowed to operate under
        """
        pass

    def Set(self, name, value):
        """
            Set Node property
        :param name:  Property name
        :param value: Property value
        """
        self.Properties[name] = value

    def Get(self, name, defaults=""):
        """
            Get Node property
        :param defaults: the default value when the proparty do not exisit
        :param name: Property name
        :return: Property value
        """
        if name in self.Properties:
            return self.Properties[name]
        return defaults

    def GentNodeTypes(self):
        """
            Get node Type
        :return: Node type value
        """
        return self.Get("NodetType")
class Agent:
    """
        An agent is main unit that host the nodes and manage its life cycle
    """

    @staticmethod
    def CreateSequentialGraph():
        graph = NodeGraph()
        graph.SetExecutionType(ExecutionType.sequential)
        return graph

    @staticmethod
    def CreateThreadedGraph():
        graph = NodeGraph()
        graph.SetExecutionType(ExecutionType.threaded)
        return graph

    @staticmethod
    def CreateParallelGraph():
        graph = NodeGraph()
        graph.SetExecutionType(ExecutionType.parallel)
        return graph

    @staticmethod
    def CreateFromJson(json):
        """
            Create an agent from a json file
            :json: the full json string to construct the graph from
        """
        raise NotImplementedError
class ExecutionType(Enum):
    all = 0
    sequential = 1
    threaded = 2
    parallel = 3
class NodeGraph:
    """
        A brain graph is a collection of nodes that work in together to a chive a goal
    """
    nodes = []
    __is_running = True
    __execution_type = ExecutionType.sequential

    def SetExecutionType(self, execution_type):
        self.__execution_type = execution_type

    def GetExecutionType(self):
        return self.__execution_type

    def __init__(self):
        """
            Initialize the graph
        """
        self.is_init = True

    def Add(self, node, name):
        """
            Add a a node to a graph
        """
        if self.GetExecutionType() == ExecutionType.parallel \
                and len(self.nodes) > 0:
            raise Exception("Parallel graph must only contain one node")

        if self.Exist(name):
            raise Exception('Pre-existing node')

        self.nodes.append({
            "Id": self.__getId(),
            "Type": node.Properties["NodeType"],
            "Name": name,
            "Node": node,
            "Connect": []
        })
        messagedb.Singletone().Write(np.zeros(1), name)

    def Exist(self, name):
        """
            Test to see if a noe with an name exists
         """
        node = [n for n in self.nodes if n['Name'] == name]
        return len(node) > 1

    def Get(self, name):
        """
            Get a node with a  specific name
        """
        node = [n for n in self.nodes if n['Name'] == name]
        if len(node) == 0:
            raise Exception('Node do not exist')
        return node[0]

    def Connect(self, node1, node2):
        """
         Add a node with name to list of connections that
         the graph will post the message to when the run is successful
         :node1: the upstream node name
         :node2: the downstream node name
        """
        try:
            [n['Connect'].append(node2) for n in self.nodes if n['Name'] == node1]
        except:
            raise Exception('Fail to connect')

    def Run(self):
        """
             loop throw all nodes and
             get any message that is active for that node and
             invoke run for that node
             then invoke post
         """

        if not self.is_init:
            raise Exception('Graph must be initaized first befor running')
        if self.GetExecutionType() == ExecutionType.sequential:
            [self.__runnode(n) for n in self.nodes]
        elif self.GetExecutionType() == ExecutionType.threaded:
            [threading.Thread(target=self.__runnode(n)).start() for n in self.nodes]
        else:
            [Process(target=self.__loop(n)).start() for n in self.nodes]

    def Stop(self):
        """
            Stop all running threads
        """
        self.__is_running = False

    def __loop(self, node):
        """
        Loop throw the run cycle till stop
        :param node: the node name to loop
        """
        while self.__is_running:
            self.__runnode(node)

    def __runnode(self, node):
        """
            This private method will get the message invoke run and post the message back
            :node: run a node with a specific name
        """
        if messagedb.Singletone().IsActive(node['Name']):
            payload = messagedb.Singletone().Read(node['Name'])
            result = node['Node'].Run(payload)
            [self.Post(c, result) for c in node['Connect']]

    def Post(self, connection, payload: object):
        """
            Post a message to a specific connection
            :connection: name of the downstream node
            :payload: the data payload that will be posted
         """
        messagedb.Singletone().Write(payload, connection)

    def UpdateValue(self, name, value):
        """
          Update the node value to a new value
         """
        node = self.Get(name)
        self.Update(node, 'Value', value)

    def Update(self, node, attribute, value):
        """
            Update the node attribute
        :param node: node name
        :param attribute: node attribute
        :param value: attribute value
        """
        node[attribute] = value

    def __getId(self):
        """
            Get a unique ID
        :return: UUID
        """
        return uuid.uuid1()
