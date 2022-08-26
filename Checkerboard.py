from typing import Optional

import numpy as np

from psychopy.visual import Window
from psychopy.visual.grating import GratingStim


class Checkerboard(GratingStim):
    def __init__(self, win: Window, size: tuple, pos: Optional[tuple] = None):
        if not pos:
            pos = [0, 0]
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
