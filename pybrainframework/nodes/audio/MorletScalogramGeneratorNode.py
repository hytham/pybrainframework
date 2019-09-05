import matplotlib.pyplot as plt
from obspy.signal.tf_misfit import cwt

from pybrainframework import BrainNode
import numpy as np


def _generate_morlet_scalogram(signal):
    """ Generate morelet scalogram from a numpy signal"""
    axis = signal.ndim - 1
    signal_length = signal.shape[axis]
    t = np.linspace(0, signal_length, signal_length)

    f_min = 1
    f_max = signal_length
    scalogram = cwt(signal, 0.001, 5, f_min, f_max)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x, y = np.meshgrid(t, np.logspace(np.log10(f_min), np.log10(f_max), scalogram.shape[0]))

    ax.pcolormesh(x, y, np.abs(scalogram), cmap='hot')
    ax.set_yscale('log')
    ax.set_ylim(f_min, f_max)
    ax.axis('off')
    ax.set_axis_off()
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    return data.reshape(fig.canvas.get_width_height()[::-1] + (3,))


class MoreletScalogramGeneratorNode(BrainNode):
    def Init(self):
        pass

    def Stop(self):
        pass

    def Unload(self):
        pass

    def __init__(self, logger):
        super().__init__("morlet_scalogram_generator", logger)

    def Load(self):
        pass

    def Run(self, np_array):
        return _generate_morlet_scalogram(np_array)

    def GetAllowedExecutionType(self):
        return ExecutionType.all
