import unittest

import pandas as pd

from data_generation.inject_faults import inject_faults
from data_generation.simulate_satellite import simulate_dataset


class FaultInjectionTests(unittest.TestCase):
    def test_fault_labels_added(self):
        df = simulate_dataset(samples_per_satellite=300)
        out = inject_faults(df)
        labels = set(out["fault_class"].dropna().unique())
        self.assertIn("POWER_SPIKE", labels)
        self.assertIn("THERMAL_DRIFT", labels)
        self.assertIn("VOLTAGE_DROP", labels)
        self.assertIn("WHEEL_OSCILLATION", labels)
        self.assertIn("SENSOR_DROPOUT", labels)


if __name__ == "__main__":
    unittest.main()
