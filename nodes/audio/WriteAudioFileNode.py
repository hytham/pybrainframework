from librosa.output import write_wav

from BrainFramework import BrainNode, ExecutionType


class WriteAudioFileNode(BrainNode):
    def __init__(self, logger):
        super().__init__("writeaudiofile", logger)
        
    def Load(self):
        pass

    def Run(self, np_array):
        file_name = self.Get("filename", "sample.wav")
        sr = self.Get("samplerate", "9600")
        ft = self.Get("filetype", "wav")
        if ft == "wav":
            write_wav(file_name, np_array, int(sr))

    def GetAllowedExecutionType(self):
        return [ExecutionType.threaded]
