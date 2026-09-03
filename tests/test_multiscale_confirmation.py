import unittest

from src.multiscale_confirmation import (
    BASELINE,
    CANDIDATE,
    CONFIRMATION_SEEDS,
    confirmation_metrics,
)
from src.multiscale_experiment import DEVELOPMENT_SEEDS


class MultiscaleConfirmationTests(unittest.TestCase):
    def test_confirmation_seeds_are_new(self) -> None:
        prior_seeds = {11, 23, 37, 53, 71, *DEVELOPMENT_SEEDS}
        self.assertTrue(set(CONFIRMATION_SEEDS).isdisjoint(prior_seeds))
        self.assertEqual(len(set(CONFIRMATION_SEEDS)), 5)

    def test_models_are_frozen(self) -> None:
        self.assertEqual((BASELINE.state_count, BASELINE.fast_rate), (1, 1.6))
        self.assertEqual(
            (CANDIDATE.state_count, CANDIDATE.slow_rate, CANDIDATE.fast_rate, CANDIDATE.fast_weight),
            (2, 1.2, 2.0, 0.5),
        )

    def test_confirmation_rule_requires_interval_and_guardrails(self) -> None:
        rows = []
        for task in ("kontinuitaet", "zeitskalen"):
            for seed in CONFIRMATION_SEEDS:
                for noise in (0.15, 0.35, 0.55):
                    rows.append({"task": task, "seed": seed, "noise_sigma": noise, "model": BASELINE.name, "accuracy": 0.70})
                    rows.append({"task": task, "seed": seed, "noise_sigma": noise, "model": CANDIDATE.name, "accuracy": 0.73})
        metrics = confirmation_metrics(rows)
        self.assertTrue(metrics["success"])


if __name__ == "__main__":
    unittest.main()

