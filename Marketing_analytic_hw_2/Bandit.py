"""Compare epsilon-greedy and Gaussian Thompson Sampling on four advertisements.

Run ``python Bandit.py`` to reproduce the CSV, figures, and logged results.
Rewards are Normal(mean=p, variance=1/precision), not binary clicks.
"""
from abc import ABC, abstractmethod
import csv
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from loguru import logger


class Bandit(ABC):
    ##==== DO NOT REMOVE ANYTHING FROM THIS CLASS ====##

    @abstractmethod
    def __init__(self, p):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def pull(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def experiment(self):
        pass

    @abstractmethod
    def report(self):
        # store data in csv
        # print average reward (use f strings to make it informative)
        # print average regret (use f strings to make it informative)
        pass

    def _setup(self, p, trials, precision, seed):
        """Allocate experiment state; p contains the true reward means."""
        self.p = np.asarray(p, dtype=float)
        if self.p.ndim != 1 or not self.p.size or not np.isfinite(self.p).all():
            raise ValueError("p must be a nonempty sequence of finite reward means.")
        if not isinstance(trials, int) or trials < self.p.size:
            raise ValueError("trials must be an integer at least as large as the arm count.")
        if not np.isfinite(precision) or precision <= 0:
            raise ValueError("precision must be positive and finite.")
        self.trials, self.precision, self.seed = trials, precision, seed
        self.rng = np.random.default_rng(seed)
        self.counts = np.zeros(self.p.size, dtype=int)
        self.means = np.zeros(self.p.size)
        self.choices = np.zeros(trials, dtype=int)
        self.rewards = np.zeros(trials)
        self.regrets = np.zeros(trials)
        self.history = np.zeros((trials, self.p.size))
        self.t = 0

    def _observe(self, arm):
        """Draw the selected arm's reward, without exposing other arms to the policy."""
        self.arm = int(arm)
        self.reward = float(self.reward_table[self.t, self.arm])
        return self.reward

    def _run(self, reward_table=None):
        """Run once. A shared reward table gives both policies the same environment."""
        if self.t:
            raise RuntimeError("Create a new algorithm instance for a new experiment.")
        if reward_table is None:
            environment = np.random.default_rng(self.seed + 1)
            reward_table = environment.normal(
                self.p, 1 / np.sqrt(self.precision), (self.trials, self.p.size)
            )
        self.reward_table = np.asarray(reward_table, dtype=float)
        if self.reward_table.shape != (self.trials, self.p.size):
            raise ValueError("reward_table must have one row per trial and one column per arm.")
        if not np.isfinite(self.reward_table).all():
            raise ValueError("reward_table must contain finite rewards.")
        for t in range(self.trials):
            self.t = t
            self.pull()
            self.update()
            self.choices[t] = self.arm
            self.rewards[t] = self.reward
            # Expected regret avoids treating random reward noise as a decision error.
            self.regrets[t] = self.p.max() - self.p[self.arm]
            self.history[t] = self.means
        self.t = self.trials
        return self

    def _report(self, csv_path):
        """Append this algorithm's observations and log totals and per-trial averages."""
        if self.t != self.trials:
            raise RuntimeError("Run experiment() before report().")
        csv_path = Path(csv_path)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        header_needed = not csv_path.exists() or csv_path.stat().st_size == 0
        with csv_path.open("a", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            if header_needed:
                writer.writerow(["Bandit", "Reward", "Algorithm"])
            writer.writerows(
                (int(arm) + 1, float(reward), type(self).__name__)
                for arm, reward in zip(self.choices, self.rewards)
            )
        logger.info(f"{self!r}: cumulative reward = {self.rewards.sum():.4f}; "
                    f"average reward = {self.rewards.mean():.6f}")
        logger.info(f"{type(self).__name__}: cumulative regret = {self.regrets.sum():.4f}; "
                    f"average regret = {self.regrets.mean():.6f}")
        logger.info(f"{type(self).__name__}: pulls per bandit = {self.counts.tolist()}")


class Visualization:
    """Save the learning curves and the two cumulative comparisons."""

    def __init__(self, algorithms, output_dir):
        self.algorithms = algorithms
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot1(self):
        """Show each arm's estimated mean on linear and logarithmic trial axes."""
        for algorithm in self.algorithms:
            fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
            trials = np.arange(1, algorithm.trials + 1)
            for ax, scale in zip(axes, ("linear", "log")):
                for arm, true_mean in enumerate(algorithm.p):
                    line, = ax.plot(trials, algorithm.history[:, arm],
                                    label=f"Bandit {arm + 1}", linewidth=1.2)
                    ax.axhline(true_mean, color=line.get_color(), linestyle="--", alpha=0.5)
                ax.set(xscale=scale, xlabel=f"Trial ({scale} scale)", ylabel="Estimated mean reward")
                ax.grid(alpha=0.2)
            axes[0].legend(loc="lower right", ncol=2)
            fig.suptitle(f"{type(algorithm).__name__}: learning the reward means\n"
                         "Dashed lines show the true means")
            fig.savefig(self.output_dir / f"{type(algorithm).__name__}_learning.png", dpi=180)
            plt.close(fig)

    def plot2(self):
        """Compare cumulative realized reward and cumulative expected regret."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
        for algorithm in self.algorithms:
            trials = np.arange(1, algorithm.trials + 1)
            axes[0].plot(trials, np.cumsum(algorithm.rewards), label=type(algorithm).__name__)
            axes[1].plot(trials, np.cumsum(algorithm.regrets), label=type(algorithm).__name__)
        for ax, label in zip(axes, ("Cumulative reward", "Cumulative expected regret")):
            ax.set(xlabel="Trial", ylabel=label, title=label)
            ax.legend()
            ax.grid(alpha=0.2)
        fig.savefig(self.output_dir / "comparison.png", dpi=180)
        plt.close(fig)


class EpsilonGreedy(Bandit):
    """Explore with probability 1/t; otherwise select the largest sample mean."""

    def __init__(self, p, trials=20000, precision=1.0, seed=42):
        """Set reward means, trial count, known reward precision, and policy seed."""
        self._setup(p, trials, precision, seed)

    def __repr__(self):
        return f"EpsilonGreedy(epsilon=1/t, trials={self.trials})"

    def pull(self):
        """Try every arm once, then explore or exploit with random tie-breaking."""
        if self.t < self.p.size:
            arm = self.t
        elif self.rng.random() < 1.0 / (self.t + 1):
            arm = self.rng.integers(self.p.size)
        else:
            arm = self.rng.choice(np.flatnonzero(self.means == self.means.max()))
        return self._observe(arm)

    def update(self):
        """Update the selected arm's running sample mean."""
        self.counts[self.arm] += 1
        self.means[self.arm] += (self.reward - self.means[self.arm]) / self.counts[self.arm]

    def experiment(self, reward_table=None):
        """Run the epsilon-greedy experiment and return its recorded results."""
        return self._run(reward_table)

    def report(self, csv_path="data/rewards.csv"):
        """Append rewards to CSV and log cumulative and average performance."""
        self._report(csv_path)


class ThompsonSampling(Bandit):
    """Use a Normal prior for each unknown mean with known observation precision."""

    def __init__(self, p, trials=20000, precision=1.0, seed=43):
        """Start each arm at Normal(0, 1), with prior precision equal to one."""
        self._setup(p, trials, precision, seed)
        self.posterior_precision = np.ones(self.p.size)

    def __repr__(self):
        return f"ThompsonSampling(precision={self.precision}, trials={self.trials})"

    def pull(self):
        """Sample each arm's mean from its posterior and select the largest draw."""
        samples = self.rng.normal(self.means, 1 / np.sqrt(self.posterior_precision))
        return self._observe(np.argmax(samples))

    def update(self):
        """Apply the conjugate Normal update using only the observed reward."""
        arm = self.arm
        old_precision = self.posterior_precision[arm]
        new_precision = old_precision + self.precision
        self.means[arm] = (old_precision * self.means[arm] + self.precision * self.reward) / new_precision
        self.posterior_precision[arm] = new_precision
        self.counts[arm] += 1

    def experiment(self, reward_table=None):
        """Run the Thompson Sampling experiment and return its recorded results."""
        return self._run(reward_table)

    def report(self, csv_path="data/rewards.csv"):
        """Append rewards to CSV and log cumulative and average performance."""
        self._report(csv_path)


def comparison(output_dir=None):
    """Run both policies for 20,000 trials and save exactly one combined reward CSV."""
    output_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parent
    output_dir.mkdir(parents=True, exist_ok=True)
    bandit_reward = [1, 2, 3, 4]
    number_of_trials = 20000
    precision = 1.0
    environment = np.random.default_rng(2026)
    reward_table = environment.normal(
        bandit_reward, 1 / np.sqrt(precision), (number_of_trials, len(bandit_reward))
    )
    algorithms = [EpsilonGreedy(bandit_reward, number_of_trials, precision),
                  ThompsonSampling(bandit_reward, number_of_trials, precision)]
    csv_path = output_dir / "data" / "rewards.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    # Re-running replaces the previous experiment instead of duplicating CSV rows.
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerow(["Bandit", "Reward", "Algorithm"])
    for algorithm in algorithms:
        algorithm.experiment(reward_table)
        algorithm.report(csv_path)
    visualizer = Visualization(algorithms, output_dir / "img")
    visualizer.plot1()
    visualizer.plot2()
    return algorithms


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, format="{level}: {message}", level="INFO")
    comparison()
