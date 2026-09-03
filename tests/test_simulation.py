import unittest

import numpy as np

from src.feldchip_simulation import (
    MODEL_NAMES,
    SimulationConfig,
    canonical_patterns,
    laplacian_neumann,
    return_gain,
    simulate_batch,
)


class FeldchipSimulationTests(unittest.TestCase):
    def test_laplacian_of_constant_field_is_zero(self) -> None:
        field = np.ones((3, 4, 4))
        np.testing.assert_allclose(laplacian_neumann(field), 0.0)

    def test_all_required_patterns_exist(self) -> None:
        patterns = canonical_patterns()
        self.assertEqual(len(patterns), 6)
        self.assertTrue(all(value.shape == (4, 4) for value in patterns.values()))

    def test_regime_gain_is_monotonic(self) -> None:
        amplitudes = np.linspace(0.0, 3.0, 301)
        config = SimulationConfig()
        for variant in ("feld_2_regime", "feld_3_regime", "feld_4_regime", "feld_glatt"):
            gain = return_gain(amplitudes, variant, config)
            self.assertTrue(np.all(np.diff(gain) >= -1e-12), variant)

    def test_dynamic_models_respect_hard_limit(self) -> None:
        stimulus = np.full((4, 4, 4), 20.0)
        config = SimulationConfig(stimulus_time=0.4, return_time=0.4)
        for variant in MODEL_NAMES[:6]:
            response, _ = simulate_batch(stimulus, variant, np.random.default_rng(7), config)
            self.assertLessEqual(float(np.max(np.abs(response))), config.hard_limit)

    def test_zero_input_returns_close_to_reference(self) -> None:
        stimulus = np.zeros((8, 4, 4))
        config = SimulationConfig(stimulus_time=0.2, return_time=3.0)
        _, metrics = simulate_batch(stimulus, "feld_3_regime", np.random.default_rng(5), config)
        self.assertLess(metrics["return_residual"], 0.08)

    def test_same_seed_produces_same_response(self) -> None:
        stimulus = np.stack([canonical_patterns()["kreuz"]] * 3)
        config = SimulationConfig(stimulus_time=0.2, return_time=0.2)
        first, first_metrics = simulate_batch(
            stimulus, "feld_glatt", np.random.default_rng(19), config
        )
        second, second_metrics = simulate_batch(
            stimulus, "feld_glatt", np.random.default_rng(19), config
        )
        np.testing.assert_array_equal(first, second)
        self.assertEqual(first_metrics, second_metrics)


if __name__ == "__main__":
    unittest.main()
