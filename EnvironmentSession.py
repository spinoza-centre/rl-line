import numpy as np

from exptools2.core import Session

from Color import Color
from EnvironmentTrial import EnvironmentTrial
from WaitingTrial import WaitingTrial


class EnvironmentSession(Session):
    def __init__(self, output_str, n_trials, output_dir=None, settings_file=None):
        super().__init__(output_str, output_dir, settings_file=settings_file)
        self.n_trials = n_trials
        self.trials = []

    def create_trials(self, durations=(.5, .5)):
        red_environment = [
            EnvironmentTrial(session=self,
                             trial_nr=trial_nr,
                             phase_durations=durations,
                             color=Color.RED.value)
            for trial_nr in range(self.n_trials // 2)]
        green_environment = [
            EnvironmentTrial(session=self,
                             trial_nr=trial_nr,
                             phase_durations=durations,
                             color=Color.GREEN.value)
            for trial_nr in range(self.n_trials // 2)]

        trials = np.random.choice(np.concatenate([red_environment, green_environment]), self.n_trials,
                                  replace=False)

        self.trials = trials
      # self.trials = [WaitingTrial(self, -999, (24, 0)), *trials, WaitingTrial(self, -999, (24, 0))]

    def run(self):
        self.start_experiment()
        for trial in self.trials:
            trial.run()

        self.close()
