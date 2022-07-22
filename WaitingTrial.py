from exptools2.core import Trial


class WaitingTrial(Trial):
    def __init__(self, session, trial_nr, phase_durations):
        super(WaitingTrial, self).__init__(session=session, trial_nr=trial_nr, phase_durations=phase_durations)

    def draw(self):
        self.session.win.flip()
