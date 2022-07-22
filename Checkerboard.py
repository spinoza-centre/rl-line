import numpy as np
from psychopy.visual.grating import GratingStim


class Checkerboard(GratingStim):
    def __init__(self, win, size, pos):
        super(Checkerboard, self).__init__(win=win, size=size, pos=pos)

        checkerboard = np.array([
            [1, -1, 1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1, -1, 1],
            [1, -1, 1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1, -1, 1],
            [1, -1, 1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1, -1, 1],
            [1, -1, 1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1, -1, 1]
        ])

        self.tex = checkerboard
