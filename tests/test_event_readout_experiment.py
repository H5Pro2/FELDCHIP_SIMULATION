import unittest

import numpy as np

from src.event_readout_experiment import (
    EVENT_READOUT_SEEDS,
    EventReadoutCandidate,
    event_readout,
    event_readout_candidates,
    normalized_compact_channels,
    normalized_temporal_readout,
    select_event_readout,
)


class EventReadoutExperimentTests(unittest.TestCase):
    def test_candidate_grid_has_twelve_unique_readouts(self) -> None:
        candidates = event_readout_candidates()
        self.assertEqual(len(candidates), 12)
        self.assertEqual(len({candidate.name for candidate in candidates}), 12)

    def test_event_seeds_are_new(self) -> None:
        previous = {11, 23, 37, 53, 71, 101, 131, 167, 211, 241, 277, 313, 349, 401, 431, 463}
        self.assertTrue(set(EVENT_READOUT_SEEDS).isdisjoint(previous))

    def test_normalized_readouts_are_finite_and_bounded(self) -> None:
        rng = np.random.default_rng(17)
        fields = rng.uniform(-3.0, 3.0, size=(5, 80, 4, 4))
        channels = normalized_compact_channels(fields)
        features = normalized_temporal_readout(fields)
        self.assertEqual(channels.shape, (5, 80, 8))
        self.assertEqual(features.shape, (5, 16))
        self.assertTrue(np.all(np.isfinite(features)))
        self.assertLessEqual(float(np.max(np.abs(channels))), 1.0)

    def test_zero_field_has_no_events(self) -> None:
        candidate = event_readout_candidates()[0]
        features, activity = event_readout(np.zeros((3, 80, 4, 4)), candidate)
        self.assertEqual(features.shape, (3, 16))
        self.assertTrue(np.all(features == 0.0))
        self.assertEqual(activity, 0.0)

    def test_constant_field_only_has_initial_quantization_events(self) -> None:
        candidate = EventReadoutCandidate("kontrolle", 0.1, 0.0)
        short_features, short_activity = event_readout(np.ones((2, 20, 4, 4)), candidate)
        long_features, long_activity = event_readout(np.ones((2, 80, 4, 4)), candidate)
        np.testing.assert_array_equal(short_features, long_features)
        self.assertEqual(short_activity, long_activity)

    def test_event_readout_is_reproducible(self) -> None:
        fields = np.random.default_rng(29).normal(0.0, 0.4, size=(4, 80, 4, 4))
        candidate = event_readout_candidates()[5]
        first = event_readout(fields, candidate)
        second = event_readout(fields, candidate)
        np.testing.assert_array_equal(first[0], second[0])
        self.assertEqual(first[1], second[1])

    def test_selection_requires_both_controls_and_guardrails(self) -> None:
        common = {
            "threshold": 0.1,
            "decay_rate": 1.6,
            "mean_event_activity": 20.0,
            "minimum_task_advantage": 0.01,
            "minimum_noise_advantage": 0.01,
        }
        accepted = {**common, "readout": "akzeptiert", "conservative_advantage": 0.03}
        rejected = {**common, "readout": "abgelehnt", "conservative_advantage": 0.04, "minimum_noise_advantage": -0.01}
        self.assertEqual(select_event_readout([rejected, accepted]), "akzeptiert")


if __name__ == "__main__":
    unittest.main()
