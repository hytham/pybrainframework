from abc import ABC

import librosa

from BrainFramework import BrainNode, ExecutionType


class ReadAudioFileNode(BrainNode):
    """ This node will read  an audio file and send it down stream"""
    def __init__(self, logger):
        super().__init__("readaudiofile", logger)

    def Load(self):
        """ Load the audio file """
        file_path = self.Get("filename", "sample.wav")
        if file_path == "":
            self.logger.log_e("file path must be set")
            raise Exception("Missing required attribute to be set")
        self.y, self.s = librosa.load(file_path)


    def Run(self, np_array):
        """ the code to be triggered when agent is running """
        return self.y

    def GetAllowedExecutionType(self):
        return [ExecutionType.threaded]
