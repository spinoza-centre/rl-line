import argparse


def create_arguments():
    parser = argparse.ArgumentParser()

    window_group = parser.add_argument_group('window')
    window_group.add_argument('--window-monitor', type=str)
    window_group.add_argument('--window-size', type=int, nargs=2)
    window_group.add_argument('--window-distance', type=float)
    window_group.add_argument('--window-width', type=float)
    window_group.add_argument('--window-fullscreen', action=argparse.BooleanOptionalAction)

    environment_group = parser.add_argument_group('environment')
    environment_group.add_argument('--environment-first-color', type=str)
    environment_group.add_argument('--environment-first-frequency', type=int, nargs='+')
    environment_group.add_argument('--environment-second-color', type=str)
    environment_group.add_argument('--environment-second-frequency', type=int, nargs='+')

    checkerboard_group = parser.add_argument_group('checkerboard')
    checkerboard_group.add_argument('--checkerboard-size', type=int)
    checkerboard_group.add_argument('--checkerboard-first-position', type=int, nargs=2)
    checkerboard_group.add_argument('--checkerboard-second-position', type=int, nargs=2)

    experiment_group = parser.add_argument_group('experiment')
    experiment_group.add_argument('--experiment-name', type=str)
    experiment_group.add_argument('--experiment-probability', type=float)
    experiment_group.add_argument('--experiment-slice', type=int)
    experiment_group.add_argument('--experiment-intro-wait', type=float)
    experiment_group.add_argument('--experiment-outro-wait', type=float)
    experiment_group.add_argument('--experiment-left-key', type=str)
    experiment_group.add_argument('--experiment-right-key', type=str)
    experiment_group.add_argument('--experiment-keypress-wait', type=int)
    experiment_group.add_argument('--experiment-checkerboard-wait', type=int)

    args = parser.parse_args()
    return args


def parse_arguments():
    args = create_arguments()

    settings = {
        'window': {},
        'environment': {},
        'checkerboard': {},
        'experiment': {}
    }

    for arg in vars(args):
        value = getattr(args, arg)
        if value is not None:
            if arg == 'window_monitor':
                settings['window']['monitor'] = value
            if arg == 'window_size':
                settings['window']['size'] = value
            if arg == 'window_distance':
                settings['window']['distance'] = value
            if arg == 'window_width':
                settings['window']['width'] = value
            if arg == 'window_fullscreen':
                settings['window']['fullscreen'] = value

            if arg == 'environment_first_color':
                settings['environment']['first_color'] = value
            elif arg == 'environment_first_frequency':
                settings['environment']['first_frequency'] = value
            elif arg == 'environment_second_color':
                settings['environment']['second_color'] = value
            elif arg == 'environment_second_frequency':
                settings['environment']['second_frequency'] = value

            elif arg == 'checkerboard_size':
                settings['checkerboard']['size'] = value
            elif arg == 'checkerboard_first_position':
                settings['checkerboard']['first_position'] = value
            elif arg == 'checkerboard_second_position':
                settings['checkerboard']['second_position'] = value

            elif arg == 'experiment_name':
                settings['experiment']['name'] = value
            elif arg == 'experiment_probability':
                settings['experiment']['probability'] = value
            elif arg == 'experiment_slice':
                settings['experiment']['slice'] = value
            elif arg == 'experiment_intro_wait':
                settings['experiment']['intro_wait'] = value
            elif arg == 'experiment_outro_wait':
                settings['experiment']['outro_wait'] = value
            elif arg == 'experiment_left_key':
                settings['experiment']['left_key'] = value
            elif arg == 'experiment_right_key':
                settings['experiment']['right_key'] = value
            elif arg == 'experiment_keypress_wait':
                settings['experiment']['keypress_wait'] = value
            elif arg == 'experiment_checkerboard_wait':
                settings['experiment']['checkerboard_wait'] = value

    return settings
