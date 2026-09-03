import unittest

import numpy as np

from src.adaptation_experiment import (
    ADAPTATION_SEEDS,
    AdaptationCandidate,
    adaptation_candidates,
    canonical_adaptation_sequences,
    select_candidate,
    simulate_technical_return,
    simulate_temporal_candidate,
)
from src.feldchip_simulation import SimulationConfig


class AdaptationExperimentTests(unittest.TestCase):
    def test_candidate_grid_has_one_baseline_and_24_candidates(self) -> None:
        candidates = adaptation_candidates()
        self.assertEqual(len(candidates), 25)
        self.assertEqual(sum(candidate.state_count == 1 for candidate in candidates), 1)
        self.assertEqual(len({candidate.name for candidate in candidates}), 25)

    def test_new_seeds_are_unique(self) -> None:
        previous = {11, 23, 37, 53, 71, 101, 131, 167, 211, 241, 277, 313, 349}
        self.assertTrue(set(ADAPTATION_SEEDS).isdisjoint(previous))

    def test_adaptation_pairs_have_equal_absolute_energy(self) -> None:
        sequences = canonical_adaptation_sequences()
        names = tuple(sequences)
        self.assertEqual(len(names), 10)
        for index in range(0, 10, 2):
            self.assertAlmostEqual(
                float(np.sum(np.abs(sequences[names[index]]))),
                float(np.sum(np.abs(sequences[names[index + 1]]))),
            )

    def test_adaptive_output_is_reproducible_and_bounded(self) -> None:
        inputs = np.stack(tuple(canonical_adaptation_sequences().values())[:2])
        candidate = adaptation_candidates()[1]
        config = SimulationConfig()
        first = simulate_temporal_candidate(inputs, candidate, np.random.default_rng(41), config)
        second = simulate_temporal_candidate(inputs, candidate, np.random.default_rng(41), config)
        np.testing.assert_array_equal(first, second)
        self.assertLessEqual(float(np.max(np.abs(first))), 3.0)

    def test_adaptation_feedback_is_active_during_technical_return(self) -> None:
        disconnected = AdaptationCandidate("ohne_rueckwirkung", 0.9, 0.0, 1.0, 2)
        connected = AdaptationCandidate("mit_rueckwirkung", 0.9, 1.0, 1.0, 2)
        first = simulate_technical_return(disconnected, "nominal", 401, 0.02, False)
        second = simulate_technical_return(connected, "nominal", 401, 0.02, False)
        self.assertNotEqual(first["residual_p95"], second["residual_p95"])

    def test_selection_rejects_negative_task_guard(self) -> None:
        common = {
            "ci95_low": 0.0, "ci95_high": 0.1, "advantage_kontinuitaet": 0.01,
            "advantage_zeitskalen": 0.01, "advantage_noise_015": 0.02,
            "advantage_noise_035": 0.02, "advantage_noise_055": 0.02,
            "feedback_strength": 0.5, "adaptation_rate": 0.9, "adaptation_limit": 0.5,
        }
        accepted = {"model": "akzeptiert", "advantage": 0.03, "advantage_adaptation": 0.03, **common}
        rejected = {"model": "abgelehnt", "advantage": 0.04, "advantage_adaptation": -0.01, **common}
        self.assertEqual(select_candidate([rejected, accepted]), "akzeptiert")


if __name__ == "__main__":
    unittest.main()
