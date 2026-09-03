import unittest

import numpy as np

from src.anisotropic_experiment import (
    coupling_candidates,
    select_candidate,
    simulate_temporal_candidate,
    weighted_coupling,
)
from src.feldchip_simulation import SimulationConfig, laplacian_neumann
from src.temporal_experiment import canonical_sequences


class AnisotropicExperimentTests(unittest.TestCase):
    def test_candidate_grid_has_26_unique_models(self) -> None:
        candidates = coupling_candidates()
        self.assertEqual(len(candidates), 26)
        self.assertEqual(len({candidate.name for candidate in candidates}), 26)
        counts = {family: sum(candidate.family == family for candidate in candidates) for family in {candidate.family for candidate in candidates}}
        self.assertEqual(counts, {"baseline": 1, "isotrop": 1, "anisotrop": 8, "gerichtet": 16})

    def test_constant_field_has_zero_weighted_coupling(self) -> None:
        field = np.ones((3, 4, 4))
        for candidate in coupling_candidates():
            np.testing.assert_allclose(weighted_coupling(field, candidate), 0.0)

    def test_isotropic_control_matches_existing_laplacian(self) -> None:
        rng = np.random.default_rng(17)
        field = rng.normal(size=(3, 4, 4))
        isotropic = next(candidate for candidate in coupling_candidates() if candidate.family == "isotrop")
        np.testing.assert_allclose(weighted_coupling(field, isotropic), 0.34 * laplacian_neumann(field))

    def test_temporal_candidate_is_reproducible_and_bounded(self) -> None:
        sequences = canonical_sequences()
        inputs = np.stack((sequences["punkt_links_rechts"], sequences["punkt_rechts_links"]))
        candidate = next(candidate for candidate in coupling_candidates() if candidate.family == "gerichtet")
        config = SimulationConfig()
        first = simulate_temporal_candidate(inputs, candidate, np.random.default_rng(29), config)
        second = simulate_temporal_candidate(inputs, candidate, np.random.default_rng(29), config)
        np.testing.assert_array_equal(first, second)
        self.assertLessEqual(float(np.max(np.abs(first))), 3.0)

    def test_selection_rule_prefers_larger_advantage(self) -> None:
        base = {
            "mean_accuracy": 0.8, "ci95_low": -0.1, "ci95_high": 0.1,
            "advantage_noise_015": 0.01, "advantage_noise_035": 0.01,
            "advantage_noise_055": 0.01,
        }
        rows = [
            {"model": "a", "family": "anisotrop", "advantage": 0.03, "weight_sum": 1.0, **base},
            {"model": "b", "family": "gerichtet", "advantage": 0.04, "weight_sum": 0.8, **base},
        ]
        self.assertEqual(select_candidate(rows), "b")


if __name__ == "__main__":
    unittest.main()
