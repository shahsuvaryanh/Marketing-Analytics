# Homework 2: A/B Testing

Epsilon-greedy and Thompson Sampling with four advertisements and 20,000 trials per algorithm.

## Project structure

```text
Marketing_analytic_hw_2/
├── Bandit.py
├── requirements.txt
├── README.MD
├── Homework 2-4.pdf
├── data/
│   └── rewards.csv
├── img/
│   ├── EpsilonGreedy_learning.png
│   ├── ThompsonSampling_learning.png
│   └── comparison.png
└── report/
    ├── report.pdf
    └── report_source.md
```

- `Bandit.py` preserves the supplied abstract class and implements both policies, reporting, and visualization.
- `data/rewards.csv` contains 20,000 observations per algorithm, with exactly the columns `Bandit`, `Reward`, and `Algorithm`. Bandit numbers run from 1 to 4.
- `img/` contains the learning curves on linear and logarithmic trial axes and the cumulative reward and regret comparison.
- [report/report.pdf](report/report.pdf) presents the experiment design, results, and bonus proposal. [report/report_source.md](report/report_source.md) is its Markdown source.
- `Homework 2-4.pdf` contains the assignment instructions.

## Setup and run

Use Python 3.10 or newer. From this homework folder, run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python Bandit.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The script logs cumulative and average reward and regret. It regenerates `data/rewards.csv` and all three figures in `img/`, replacing previous results. The fixed random seeds make the experiment reproducible. The PDF is the report for the included run.
