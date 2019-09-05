from BrainFramework import BrainNode, ExecutionType


class Const(BrainNode):
    """
     This node will set a constant value
    """

    def __init__(self, logger):
        return super().__init__("const", logger)

    def Load(self):
        super().Load()

    def Run(self, nparray):
        return nparray

    def GetAllowedExecutionType(self):
        return [ExecutionType.all]
