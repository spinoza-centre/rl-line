import os.path as op

from EnvironmentSession import EnvironmentSession

if __name__ == '__main__':
    settings = op.join(op.dirname(__file__), 'settings.yml')
    session = EnvironmentSession('sub-01', n_trials=10, settings_file=settings)
    session.create_trials(durations=(2, 0))
    session.run()
    session.quit()
