# 🔬 Minimal Experimental Framework (Pygame)

This repository provides a simple, open-source Python framework designed to quickly and flexibly run behavioral experiments (such as reaction time tasks) for academic research. It serves as a lightweight alternative to popular tools like PsychoPy, using the standard `pygame` library to handle core stimulus presentation and data logging needs with precise timing.

## 🚀 Setup & Prerequisites

* **Python 3.x**
* **Pygame Library:** You can install it using pip:
    ```bash
    pip install pygame
    ```

## ⚙️ Configuration (`config.json`)

All experiment settings and trial parameters are centrally managed via the `config.json` file. You must edit this file to define your experiment:

* `experiment_name`: Used for data file naming.
* `participant_id`: Identifier for the current session (e.g., P001).
* `screen_size`: Display resolution (e.g., [800, 600]).
* `stimulus_duration_ms`: How long the stimulus is on screen (in milliseconds).
* `fixation_duration_ms`: Duration of the fixation cross (in milliseconds).
* `trials`: An array of dictionaries, where each dictionary defines a trial's stimulus, correct response key, and condition.

## ▶️ Usage

1.  Customize the `config.json` file with your experiment details.
2.  Run the main Python script from your terminal:
    ```bash
    python run_experiment.py
    ```

## 💾 Data Output

Data is saved automatically upon completion or premature exit into a timestamped CSV file in the `/data` folder:

`data/[experiment_name]_[participant_id]_[datetime].csv`

**Example Data Columns:**

| trial\_num | participant\_id | stimulus | condition | correct\_response | response\_key | RT\_ms | accuracy |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | P999 | RED | congruent | z | z | 450 | 1 |
| 2 | P999 | BLUE | incongruent | None | None | -999 | 0 |

## 🤝 Contribution

Feel free to report issues or submit pull requests to enhance the framework (e.g., adding image or sound support, improving timing accuracy).
