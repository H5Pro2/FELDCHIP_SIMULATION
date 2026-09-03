import unittest

import numpy as np

from src.feldchip_simulation import SimulationConfig
from src.multiscale_experiment import (
    canonical_timescale_sequences,
    select_candidate,
    simulate_temporal_candidate,
    timescale_candidates,
)


class MultiscaleExperimentTests(unittest.TestCase):
    def test_candidate_grid_has_one_baseline_and_27_candidates(self) -> None:
        candidates = timescale_candidates()
        self.assertEqual(len(candidates), 28)
        self.assertEqual(sum(candidate.state_count == 1 for candidate in candidates), 1)
        self.assertEqual(len({candidate.name for candidate in candidates}), 28)

    def test_timescale_sequence_pairs_have_equal_absolute_energy(self) -> None:
        sequences = canonical_timescale_sequences()
        names = tuple(sequences)
        self.assertEqual(len(names), 10)
        for index in range(0, 10, 2):
            first = float(np.sum(np.abs(sequences[names[index]])))
            second = float(np.sum(np.abs(sequences[names[index + 1]])))
            self.assertAlmostEqual(first, second)

    def test_two_state_output_is_reproducible_and_bounded(self) -> None:
        sequences = canonical_timescale_sequences()
        inputs = np.stack(tuple(sequences.values())[:2])
        candidate = timescale_candidates()[1]
        config = SimulationConfig()
        first = simulate_temporal_candidate(inputs, candidate, np.random.default_rng(31), config)
        second = simulate_temporal_candidate(inputs, candidate, np.random.default_rng(31), config)
        np.testing.assert_array_equal(first, second)
        self.assertLessEqual(float(np.max(np.abs(first))), 3.0)

    def test_selection_requires_both_tasks_and_all_noise_levels(self) -> None:
        common = {
            "mean_accuracy": 0.9, "ci95_low": 0.0, "ci95_high": 0.1,
            "advantage_noise_015": 0.03, "advantage_noise_035": 0.03,
            "advantage_noise_055": 0.03, "rate_ratio": 3.0, "slow_weight": 0.5,
        }
        accepted = {"model": "akzeptiert", "advantage": 0.03, "advantage_kontinuitaet": 0.02, "advantage_zeitskalen": 0.04, **common}
        rejected = {"model": "abgelehnt", "advantage": 0.04, "advantage_kontinuitaet": -0.01, "advantage_zeitskalen": 0.09, **common}
        self.assertEqual(select_candidate([rejected, accepted]), "akzeptiert")

    def test_observational_tie_uses_smaller_rate_ratio(self) -> None:
        common = {
            "mean_accuracy": 0.7, "ci95_low": 0.0, "ci95_high": 0.05,
            "advantage_kontinuitaet": 0.01, "advantage_zeitskalen": 0.04,
            "advantage_noise_015": 0.02, "advantage_noise_035": 0.02,
            "advantage_noise_055": 0.02, "slow_weight": 0.5,
        }
        wider = {"model": "weiter", "advantage": 0.02384259259259259, "rate_ratio": 2.0, **common}
        narrower = {"model": "enger", "advantage": 0.02384259259259258, "rate_ratio": 1.5, **common}
        self.assertEqual(select_candidate([wider, narrower]), "enger")


if __name__ == "__main__":
    unittest.main()
