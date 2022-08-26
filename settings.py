import os.path as op

import yaml


def create_settings():
    path = op.join(op.dirname(__file__), 'settings.yml')
    settings = [
        {
            'window': {
                'monitor': 'monitor',
                'size': [1920, 1080],
                'distance': 50,
                'width': 34.5,
                'fullscreen': True
            }
        },
        {
            'environment': {
                'first_color': 'red',
                'first_frequency': [25, 25, 25, 25],
                'second_color': 'green',
                'second_frequency': [50, 50]

            }
        },
        {
            'checkerboard': {
                'size': 128,
                'first_position': [320, 180],
                'second_position': [-320, -180]
            }
        },
        {
            'experiment': {
                'name': 'rl-line-01',
                'probability': 70,
                'slice': 20,
                'intro_wait': 24,
                'outro_wait': 24
            }
        }
    ]

    with open(path, 'w') as file:
        content = ''
        for setting in settings:
            content += yaml.safe_dump(setting, default_flow_style=False, sort_keys=False)
            content += '\n'
        file.write(content[:-1])


def load_settings():
    path = op.join(op.dirname(__file__), 'settings.yml')
    exists = op.exists(path)

    if not exists:
        create_settings()

    with open(path, 'r') as file:
        settings = yaml.safe_load(file)

    return settings


def save_settings(settings: dict, path: str):
    settings = [{key: value} for key, value in settings.items()]
    print(settings)
    with open(path, 'w') as file:
        content = ''
        for setting in settings:
            content += yaml.safe_dump(setting, default_flow_style=False, sort_keys=False)
            content += '\n'
        file.write(content[:-1])


def merge_settings(file_settings: dict, args_settings: dict):
    return {
        'window': {**file_settings['window'], **args_settings['window']},
        'environment': {**file_settings['environment'], **args_settings['environment']},
        'checkerboard': {**file_settings['checkerboard'], **args_settings['checkerboard']},
        'experiment': {**file_settings['experiment'], **args_settings['experiment']}
    }
