# Homework 2: A/B Testing

## Run

Use Python 3.10 or newer. From this folder, run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python Bandit.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The script logs the cumulative and average reward and regret for each algorithm. It also creates:

- `output/rewards.csv`: 20,000 observations per algorithm, with exactly the columns `Bandit`, `Reward`, and `Algorithm`. Bandit numbers run from 1 to 4.
- `output/epsilon_greedy_learning.png`: estimated reward means on linear and logarithmic trial axes.
- `output/thompson_sampling_learning.png`: posterior reward means on linear and logarithmic trial axes.
- `output/comparison.png`: cumulative reward and regret for the two algorithms.

Running the script again replaces these results. The seeds are fixed so the experiment can be reproduced.

## 1. Bandit class

The original `Bandit` abstract class and all six abstract methods are preserved. Both algorithms inherit from it. Shared helpers handle the experiment records and reporting; each algorithm implements its own selection rule and update.

## 2. Experiment design

There are four advertisements with true mean rewards `[1, 2, 3, 4]`. Each algorithm runs for 20,000 trials. I use normally distributed rewards with known precision 1, so each arm's reward variance is 1. This fits the requirement for known precision and allows the reward means to be greater than 1.

Both algorithms use the same simulated reward table, generated with seed 2026. A row contains the possible rewards for that trial, but each algorithm observes only the reward of the arm it selects. The policies use separate random generators, with seeds 42 and 43. The true means are used to generate rewards and calculate regret, not to choose an arm.

### 2.1 Epsilon-greedy

Each arm is pulled once to give it an initial estimate. Starting with trial 5, epsilon is `1/t`, where `t` is the trial number starting at 1. With probability epsilon, the algorithm chooses an arm uniformly at random. Otherwise, it chooses the arm with the largest sample mean, breaking ties randomly. After each observation, it updates that arm's running mean.

### 2.2 Thompson Sampling

Each unknown arm mean starts with a Normal prior with mean 0 and precision 1. On each trial, the algorithm samples a possible mean from every arm's posterior and selects the largest sample.

For an observed reward `x`, the selected arm is updated using:

```text
new_precision = old_precision + reward_precision
new_mean = (old_precision * old_mean + reward_precision * x) / new_precision
```

The other arms are unchanged. The posterior standard deviation used for sampling is `1 / sqrt(new_precision)`.

## 3. Report

The learning plots show how the estimates change over time. Dashed lines mark the true means. The log-scale panels make the early trials easier to see.

Cumulative reward is the sum of observed rewards. Regret on each trial is the best true mean minus the true mean of the selected arm. Here it is `4 - selected_mean`. This measures the expected reward lost through arm selection, without adding observation noise.

The included run gives:

| Algorithm | Cumulative reward | Average reward | Cumulative regret | Average regret |
| --- | ---: | ---: | ---: | ---: |
| Epsilon-greedy | 80062.8648 | 4.003143 | 19 | 0.000950 |
| Thompson Sampling | 79997.6595 | 3.999883 | 86 | 0.004300 |

Epsilon-greedy selected bandit 4 on 19,990 trials; Thompson Sampling selected it on 19,955 trials. Epsilon-greedy had lower regret in this run. That result depends on the random observations and does not show that it is always better. Its fast epsilon decay can also leave it exploiting a poor early estimate. The observed average reward can exceed 4 because individual rewards include normal noise.

## Bonus: Better implementation plan

I would repeat the experiment across several independent seeds and compare the mean cumulative regret with uncertainty intervals. A single run can favor either policy by chance. I would also compare the required `1/t` epsilon schedule with `min(1, c/t)` for several values of `c`, chosen on separate simulation runs. A larger `c` would keep exploration active longer and could reduce the chance of committing to the wrong arm after a few noisy observations.
