# -*- coding: utf-8 -*-

"""Main module."""
import uuid
import numpy as np
import threading
from abc import ABC, abstractmethod
from __messagedb import messagedb

class Controller:
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

    def __init__(self, node_name, node_type, logger):
        """
            :node_name: The name of the node
            :type logger: a list of loggers that will be called to log any error
        """
        self.isRunning = True
        self.Properties = {
            "id": uuid.uuid1(),
            "name": "",
            "node-type": node_name,
            "tag": "",
            "_thread": threading.Thread(target=self._loop),
            "_logger": logger
        }

    def __loop(self):
        """ The node thread looper"""
        self.runStooped = False

        while self.isRunning:
            name = self.Get("Name")
            if messagedb.Singletone().IsActive(name):
                payload = messagedb.Singletone().Read(name)
                result = self.Run(payload)
                [self.Post(c, result) for c in self.Get('Connect')]

        self.runStooped = True

    def Post(self,connection, payload: object):
        """
            Post a message to a specific connection
            :connection: name of the downstream node
            :payload: the data payload that will be posted
         """
        messagedb.Singletone().Write(payload, connection)

    @abstractmethod
    def Init(self):
        """
            Called by the agent to inita;ize the states of the node
        :return:
        """
        pass

    @abstractmethod
    def Unload(self):
        """
            Called by the agent to unliad the node from the memory and any unloading
        :return:
        """
        pass

    @abstractmethod
    def DeInit(self):
        """
            called by the agent do deinitalize the node
        :return:
        """
        pass

    @abstractmethod
    def Load(self):
        """
           called by thagent to load the node in memory
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

    def Set(self, name, value):
        """
            Set Node property
        :param name:  Property name
        :param value: Property value
        """
        self.Properties[name] = value

    def Get(self, name, defaults=None):
        """
            Get Node property
        :param defaults: the default value when the property do not exist
        :param name: Property name
        :return: Property value
        """
        if name in self.Properties:
            return self.Properties[name]
        return defaults

    def GetType(self):
        """
            Get node Type
        :return: Node type value
        """
        return self.Get("node-type")

    def GetName(self):
        """
            Get the node name
        :return: the node name
        """
        return self.Get("name")

    def IsStopped(self):
        return self.isRunning

class Agent:
    """
        An agent is main unit that host the nodes and manage its life cycle
        it contain obe  (or many - for now just one) graph nodes
    """

    def __init__(self):
        self.graph = NodeGraph()

    def Start(self):
        """ Start running all nodes life cycle """

        # Load all the nodes
        [n.Load() for n in self.graph.GetNodes()]

        # Initialize all nodes
        [n.Init() for n in self.graph.GetNodes()]

        # Start the run
        [n.Get("_thread").Start() for n in self.graph.GetNodes()]

        # check if all nodes done execution
        self._waitToStop()

        # Deinitalzie all nodes
        [n.DeInit() for n in self.graph.GetNodes()]

        # Unload all nodes
        [n.Unload() for n in self.graph.GetNodes()]

        # wait for all nodes to stop

    def _waitToStop(self):
        total_nodes_stopped = 0
        while total_nodes_stopped != len(self.graph.GetNodes()):
            for n in self.graph.GetNodes():
                if ~n.IsStooped():
                    total_nodes_stopped += 1

class NodeGraph:
    """ A brain graph is a collection of nodes that work in together to a chive a goal """
    nodes = []
    __is_running = True

    def __init__(self):
        """
            Initialize the graph
        """
        self.is_init = True

    def GetNodes(self):
        """ return all nodes in the graph """
        return self.nodes

    def Add(self, node, name):
        """
            Add a a node to a graph
        """

        if self.Exist(name):
            raise Exception('Pre-existing node')

        self.nodes.append(node)

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


