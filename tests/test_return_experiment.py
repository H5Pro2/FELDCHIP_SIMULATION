import unittest

import numpy as np

from src.return_experiment import (
    ReturnCandidate,
    candidate_grid,
    feedback_gain,
    initial_displacements,
    simulate_return,
)


class ReturnExperimentTests(unittest.TestCase):
    def test_preregistered_candidate_count_and_uniqueness(self) -> None:
        candidates = candidate_grid()
        self.assertEqual(len(candidates), 87)
        self.assertEqual(len({candidate.identifier for candidate in candidates}), 87)

    def test_initial_conditions_are_complete_and_bounded(self) -> None:
        fields, names = initial_displacements()
        self.assertEqual(fields.shape, (18, 4, 4))
        self.assertEqual(len(set(names)), 18)
        self.assertLessEqual(float(np.max(np.abs(fields))), 3.0)

    def test_feedback_laws_are_monotonic(self) -> None:
        amplitudes = np.linspace(0.0, 3.0, 301)
        for law in ("konstant", "drei_regime", "glatt"):
            candidate = ReturnCandidate(law, 0.4, 1.6, 1.0, 0.34, "abweichung")
            gains = feedback_gain(amplitudes, candidate)
            self.assertTrue(np.all(np.diff(gains) >= -1e-12), law)

    def test_short_return_run_is_reproducible_and_bounded(self) -> None:
        candidate = ReturnCandidate("konstant", 1.6, 1.6, 1.0, 0.0, "abweichung")
        first = simulate_return(candidate, "nominal", 11, duration=6.0)
        second = simulate_return(candidate, "nominal", 11, duration=6.0)
        self.assertEqual(first, second)
        self.assertLessEqual(float(first["max_abs"]), 3.0)


if __name__ == "__main__":
    unittest.main()
