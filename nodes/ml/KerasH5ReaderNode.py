from BrainFramework import BrainNode, ExecutionType
from keras.models import load_model

class KerasH5ReaderNode(BrainNode):

    def __init__(self, logger):
        super().__init__("kerash5loader", logger)

    def Load(self):
        self.model_name = self.Get("h5_file_name")
        self.model_type = self.Get("h5_model_type", "full")

        if self.model_type == "full":
            self.model = model = load_model(self.model_name)

    def Run(self, np_array):
        return self.model.predict(np_array)

    def GetAllowedExecutionType(self):
        return [ExecutionType.threaded]