import unittest

import numpy as np

from src.feldchip_simulation import SimulationConfig
from src.temporal_experiment import (
    SEQUENCE_NAMES,
    canonical_sequences,
    simulate_temporal_batch,
    temporal_readout,
)


class TemporalExperimentTests(unittest.TestCase):
    def test_all_preregistered_sequences_exist(self) -> None:
        sequences = canonical_sequences()
        self.assertEqual(tuple(sequences), SEQUENCE_NAMES)
        self.assertTrue(all(value.shape == (80, 4, 4) for value in sequences.values()))

    def test_directional_sequences_are_distinct(self) -> None:
        sequences = canonical_sequences()
        self.assertFalse(np.array_equal(sequences["punkt_links_rechts"], sequences["punkt_rechts_links"]))

    def test_temporal_readout_has_sixteen_finite_channels(self) -> None:
        fields = np.stack(list(canonical_sequences().values()))
        features = temporal_readout(fields)
        self.assertEqual(features.shape, (10, 16))
        self.assertTrue(np.all(np.isfinite(features)))

    def test_temporal_dynamic_model_is_reproducible_and_bounded(self) -> None:
        inputs = np.stack(list(canonical_sequences().values())[:2])
        config = SimulationConfig()
        first, metrics_first = simulate_temporal_batch(inputs, "feld_3_regime", np.random.default_rng(17), config)
        second, metrics_second = simulate_temporal_batch(inputs, "feld_3_regime", np.random.default_rng(17), config)
        np.testing.assert_array_equal(first, second)
        self.assertEqual(metrics_first, metrics_second)
        self.assertLessEqual(float(np.max(np.abs(first))), config.hard_limit)


if __name__ == "__main__":
    unittest.main()

