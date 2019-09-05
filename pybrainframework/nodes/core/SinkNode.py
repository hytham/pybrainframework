from BrainFramework import BrainNode, ExecutionType
import numpy as np

class SinkNode(BrainNode):
    def Load(self):
        self.Set("internalvalue", np.zeros((1, 1)))

    def Run(self, np_array):
        self.Set("internalvalue", np_array)

    def GetAllowedExecutionType(self):
        return [ExecutionType.all]
