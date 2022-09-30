# Reversal Learning

## How to Install
Prerequisites:
- Python 3.9

```
pip install attrdict
pip install -r requirements.txt
```

## How to Run
```
python main.py
```

The application expects a `settings.yml` and a `isi.txt` file, if it doesn't find them, they are created from scratch.

The application supports a wide range of command line arguments, to see the full list type
```
python main.py -h
```

The applications waits a number of seconds specified in the settings (`intro_wait`) at the beginning of the experiment,
it then shows a fixation mark that changes color depending on the environment, and after a fixed amount of time it
also displays a flickering checkerboard.

![screenshot](screenshot.png)

After running all trials, it waits again for some time (`outro_wait`), displays a message and then quits.

## Data
The program collects various logs, for debugging and analysis purposes. They can be found in the `logs` folder.

- `EXPERIMENT_NAME_isi.txt` contains the inter stimulus intervals sequentially used by the program

- `EXPERIMENT_NAME_events.tsv` contains, for each trial, the environment color, the onsets for the first checkerboard
frame and the keypress, and the reward

- `EXPERIMENT_NAME_expsettings.yml` contains the settings used for the experiment

- `EXPERIMENT_NAME_log.txt` contains the PsychoPy log, useful for debugging purposes

The data present in `isi.txt`, `EXPERIMENT_NAME_events.tsv` and `EXPERIMENT_NAME_expsettings.yml` is sufficient to
full recreate the original conditions of an experiment, giving the opportunity to repeat it multiple times with the
exact same sequence and timing.
