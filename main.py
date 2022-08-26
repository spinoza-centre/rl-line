import os
import os.path as op
import random

from psychopy import colors, core, data, event, logging, monitors, visual

from Checkerboard import Checkerboard
from FixationBullsEye import FixationBullsEye
from arguments import parse_arguments
from settings import load_settings, merge_settings, save_settings


def create_window(settings):
    monitor = monitors.Monitor(settings['window']['monitor'])
    monitor.setSizePix(settings['window']['size'])
    monitor.setDistance(settings['window']['distance'])
    monitor.setWidth(settings['window']['width'])

    # create a window
    win = visual.Window(settings['window']['size'], monitor=monitor, units='pix',
                        fullscr=settings['window']['fullscreen'])
    return win


if __name__ == '__main__':
    file_settings = load_settings()
    args_settings = parse_arguments()
    settings = merge_settings(file_settings, args_settings)
    logging.console.setLevel(logging.ERROR)
    log_filename = op.join(op.dirname(__file__), 'logs', f'{settings["experiment"]["name"]}_log.txt')

    if not op.isdir('logs'):
        os.mkdir('logs')

    log_file = logging.LogFile(log_filename, level=logging.DEBUG)

    win = create_window(settings)

    core.wait(settings['experiment']['intro_wait'])

    # create some stimuli
    color = colors.Color([255, 0, 0], space='rgb255')
    fixation = FixationBullsEye(win=win, circle_radius=5, color=color)

    dot = Checkerboard(win=win, size=(128, 128), pos=None)

    environments = [
        {
            'color': settings['environment']['first_color'],
            'frequency': settings['environment']['first_frequency']
        },
        {
            'color': settings['environment']['second_color'],
            'frequency': settings['environment']['second_frequency']
        },
    ]

    trials = []
    for environment in environments:
        trial = []
        for i, frequency in enumerate(environment['frequency']):
            for _ in range(frequency):
                positive = random.random() * 100 > (100 - settings['experiment']['probability'])
                positive = positive if i % 2 else not positive
                trial += [{
                    'color': environment['color'],
                    'positive': positive,
                    'position': settings['checkerboard']['first_position'] if positive else
                    settings['checkerboard']['second_position']
                }]
        trials += [trial]

    index = 0
    trial_data = []

    while index + 5 < 101:
        for trial in trials:
            trial_data += trial[index:index + 5]
        index += 5

    experiment_handler = data.ExperimentHandler(name=settings['experiment']['name'])
    trial_handler = data.TrialHandler(trial_data, 1, method='sequential')
    trial_handler.setExp(experiment_handler)
    experiment_handler.addLoop(trial_handler)

    trial_clock, experiment_clock = core.Clock(), core.Clock()
    for trial_nr, trial in enumerate(trial_handler):
        trial_clock.reset()
        onset = False
        trial['onset'] = None
        trial['onset_abs'] = None
        trial['keypress'] = None
        trial['reward'] = None
        for frameN in range(round(4.5 * 60)):
            keys = event.getKeys(keyList=['z', 'm'])
            if keys and not onset and frameN < 120:
                trial['onset'] = trial_clock.getTime()
                trial['onset_abs'] = experiment_clock.getTime()
                trial['keypress'] = keys[0]
                trial['reward'] = 100 if (trial['positive'] and trial['keypress'] == 'z') or (
                        not trial['positive'] and trial['keypress'] == 'm') else -50
                onset = True
            if (frameN % 4) != 0 and 120 < frameN < 120 + 60 * .75:
                dot.pos = trial['position']
                dot.draw()
            fixation.set_color(colors.Color(trial['color'], space='named'))
            fixation.draw()
            win.update()

        trial['trial_nr'] = trial_nr
        trial['event_type'] = 'stim'
        trial['nr_frames'] = round(4.5 * 60)
        trial['duration'] = trial_clock.getTime()

    core.wait(settings['experiment']['outro_wait'])

    trial_handler.saveAsText(
        op.join(op.dirname(__file__), 'logs', f'{settings["experiment"]["name"]}_events.tsv'),
        stimOut=['color', 'trial_nr', 'onset', 'event_type', 'nr_frames', 'onset_abs',
                 'duration', 'keypress', 'reward'], appendFile=False, dataOut=[], fileCollisionMethod='overwrite')
    settings_filename = op.join(op.dirname(__file__), 'logs',
                                f'{settings["experiment"]["name"]}_expsettings.yml')

    save_settings(settings, settings_filename)
    experiment_handler.close()
    win.close()
    core.quit()
