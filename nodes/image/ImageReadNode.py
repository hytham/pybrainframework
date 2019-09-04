from BrainFramework import BrainNode, ExecutionType
from PIL import Image

class ImageReadNode(BrainNode):

    def __init__(self,logger):
        super(ImageReadNode, self).__init__("readimage", logger)

    def Load(self):
        file_name = self.Get("filename", "logo.jpg")
        self.im = Image.open(file_name)

    def Run(self, np_array):
        return self.im


    def GetAllowedExecutionType(self):
        return ExecutionType.threaded