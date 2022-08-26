from typing import List, Union
from typing import Optional

from psychopy import colors
from psychopy.visual import Window
from psychopy.visual.line import Line


class FixationBullsEye:
    def __init__(self, win: Window, circle_radius: int, color: Union[tuple, str, colors.Color],
                 pos: Optional[List[int]] = None):
        if pos is None:
            pos = [0, 0]
        self.color = color
        self.line1 = Line(win, start=(-circle_radius + pos[0], -circle_radius + pos[1]),
                          end=(circle_radius + pos[0], circle_radius + pos[1]), lineColor=self.color,
                          lineWidth=4)
        self.line2 = Line(win, start=(-circle_radius + pos[0], circle_radius + pos[1]),
                          end=(circle_radius + pos[0], -circle_radius + pos[1]), lineColor=self.color,
                          lineWidth=4)

    def draw(self):
        self.line1.draw()
        self.line2.draw()

    def set_color(self, color):
        self.line1.color = color
        self.line2.color = color
        self.color = color
