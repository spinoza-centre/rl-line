import random

from exptools2.core import Trial

from Checkerboard import Checkerboard
from FixationBullsEye import FixationBullsEye


class EnvironmentTrial(Trial):
    def __init__(self, session, trial_nr, phase_durations, color):
        super().__init__(session, trial_nr, phase_durations)
        self.is_positive_reward = random.random() > 0.4

        self.fixation = FixationBullsEye(win=self.session.win, circle_radius=5, color=color)

        if self.is_positive_reward:
            pos = (320, 180)
        else:
            pos = (-320, -180)

        self.dot = Checkerboard(win=self.session.win, size=(128, 128), pos=pos)

    def draw(self):
        self.dot.draw()
        self.fixation.draw()

    def create_trial(self):
        pass
