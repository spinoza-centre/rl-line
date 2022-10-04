import os
import os.path as op
import random

import numpy as np
from psychopy import colors, core, data, event, logging, monitors, visual

from Checkerboard import Checkerboard
from FixationMark import FixationMark
from arguments import parse_arguments
from settings import load_settings, merge_settings, save_settings


def interleave(a, b):
    return [x.pop(0) for x in random.sample([a] * len(a) + [b] * len(b), len(a) + len(b))]


def create_settings():
    file_settings = load_settings()
    args_settings = parse_arguments()
    return merge_settings(file_settings, args_settings)


def create_logging(settings):
    logging.console.setLevel(logging.ERROR)
    experiment_name = settings["experiment"]["name"]
    log_filename = op.join(op.dirname(__file__), 'logs', f'{experiment_name}_log.txt')
    if not op.isdir('logs'):
        os.mkdir('logs')
    _ = logging.LogFile(log_filename, level=logging.DEBUG)


def create_window(settings):
    window_monitor = settings['window']['monitor']
    window_size = settings['window']['size']
    window_distance = settings['window']['distance']
    window_width = settings['window']['width']
    window_fullscreen = settings['window']['fullscreen']

    monitor = monitors.Monitor(window_monitor)
    monitor.setSizePix(window_size)
    monitor.setDistance(window_distance)
    monitor.setWidth(window_width)

    return visual.Window(window_size, monitor=monitor, fullscr=window_fullscreen, units='pix')


def create_intervals(settings):
    experiment_name = settings['experiment']['name']

    path = op.join(op.dirname(__file__), 'isi.txt')
    exists = op.exists(path)

    if exists:
        with open(path, 'r') as file:
            isi = np.loadtxt(file)
    else:
        first_frequency = settings['environment']['first_frequency']
        second_frequency = settings['environment']['second_frequency']

        rng = np.random.default_rng()
        isi = 2 + rng.exponential(2, sum(first_frequency) + sum(second_frequency))

    isi_filename = op.join(op.dirname(__file__), 'logs', f'{experiment_name}_isi.txt')

    with open(isi_filename, 'w') as file:
        np.savetxt(file, isi, fmt='%.18f')

    return isi


def create_experiment(settings):
    first_frequency = settings['environment']['first_frequency']
    second_frequency = settings['environment']['second_frequency']
    first_color = settings['environment']['first_color']
    second_color = settings['environment']['second_color']
    experiment_name = settings['experiment']['name']
    experiment_probability = settings['experiment']['probability']
    checkerboard_first_position = settings['checkerboard']['first_position']
    checkerboard_second_position = settings['checkerboard']['second_position']

    environments = [
        {
            'color': first_color,
            'frequency': first_frequency
        },
        {
            'color': second_color,
            'frequency': second_frequency
        },
    ]

    trials = []
    for environment in environments:
        trial = []
        for i, freq in enumerate(environment['frequency']):
            for _ in range(freq):
                positive = random.random() * 100 > (100 - experiment_probability)
                positive = positive if i % 2 else not positive
                trial += [{
                    'color': environment['color'],
                    'positive': positive,
                    'position': checkerboard_first_position if positive else checkerboard_second_position
                }]
        trials += [trial]

    trial_data = interleave(trials[0], trials[1])

    experiment = data.ExperimentHandler(name=experiment_name)
    trials = data.TrialHandler(trial_data, 1, method='sequential')
    trials.setExp(experiment)
    experiment.addLoop(trials)

    return experiment


def create_stimuli(window, settings):
    color = colors.Color([255, 0, 0], space='rgb255')
    fixation_mark = FixationMark(win=window, circle_radius=5, color=color)
    checkerboard = Checkerboard(win=window, size=settings["checkerboard"]["size"], pos=None)
    return fixation_mark, checkerboard


def save_experiment(experiment, settings):
    trials = experiment.loops[0]
    experiment_name = settings["experiment"]["name"]
    stim_out = ['trial_nr', 'color', 'onset_stimulus', 'onset_stimulus_abs',
                'onset_keypress', 'onset_keypress_abs', 'reward']
    trials.saveAsText(op.join(op.dirname(__file__), 'logs', f'{experiment_name}_events.tsv'), stimOut=stim_out,
                      appendFile=False, dataOut=[], fileCollisionMethod='overwrite')
    settings_filename = op.join(op.dirname(__file__), 'logs', f'{experiment_name}_expsettings.yml')
    save_settings(settings, settings_filename)


def main():
    settings = create_settings()
    create_logging(settings)
    window = create_window(settings)
    isi = create_intervals(settings)
    experiment = create_experiment(settings)

    keypress_wait = round(settings['experiment']['keypress_wait'] / 1000 * 60)
    checkerboard_wait = round(settings['experiment']['checkerboard_wait'] / 1000 * 60)
    stimulus_duration = keypress_wait + checkerboard_wait

    intro_wait, outro_wait = settings['experiment']['intro_wait'], settings['experiment']['outro_wait']
    left_key = settings['experiment']['left_key']
    right_key = settings['experiment']['right_key']
    keys = [left_key, right_key]

    fixation_mark, checkerboard = create_stimuli(window, settings)
    trial_clock, experiment_clock = core.Clock(), core.Clock()
    trials = experiment.loops[0]
    core.wait(intro_wait)

    for trial_nr, trial in enumerate(trials):
        trial_clock.reset()
        reward = 0
        register_onset_keypress = False
        register_onset_stimulus = False
        inter_stimulus_interval = round(isi[trial_nr] * 60)
        duration = (inter_stimulus_interval + stimulus_duration)
        fixation_mark.set_color(colors.Color(trial['color'], space='named'))

        trial['onset_keypress'] = 0
        trial['onset_keypress_abs'] = 0

        for frameN in range(duration):
            # check keyboard events
            event_keys = event.getKeys(keyList=keys)
            # if registred keys are pressed, assign reward
            if event_keys and not register_onset_keypress and frameN < keypress_wait:
                register_onset_keypress = True
                trial['onset_keypress'] = trial_clock.getTime()
                trial['onset_keypress_abs'] = experiment_clock.getTime()
                keypress = event_keys[0]
                if (trial['positive'] and keypress == left_key) or (not trial['positive'] and keypress == right_key):
                    reward = 100
                else:
                    reward = -50

            # frame [4-8), [12, 16), etc. have flipped checkerboard textures
            if (frameN % 4) == 0:
                checkerboard.tex *= -1

            if keypress_wait < frameN < stimulus_duration:
                if not register_onset_stimulus:
                    register_onset_keypress = True
                    trial['onset_stimulus'] = trial_clock.getTime()
                    trial['onset_stimulus_abs'] = experiment_clock.getTime()

                checkerboard.pos = trial['position']
                checkerboard.draw()

            if frameN >= stimulus_duration:
                fixation_mark.set_color(colors.Color('white', space='named'))

            fixation_mark.draw()
            window.update()

        trial['trial_nr'] = trial_nr
        trial['reward'] = reward

    core.wait(outro_wait)

    save_experiment(experiment, settings)
    experiment.close()
    window.close()
    core.quit()


if __name__ == '__main__':
    main()
