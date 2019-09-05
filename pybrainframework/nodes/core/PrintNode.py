from BrainFramework import BrainNode, ExecutionType


class PrintNode(BrainNode):
    def __init__(self, logger):
        super().__init__("print", logger)

    def Load(self):
        pass

    def Run(self, np_array):
        print(np_array)

    def GetAllowedExecutionType(self):
        return [ExecutionType.all]
