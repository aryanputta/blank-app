import unittest

from data_generation.simulate_satellite import simulate_dataset


class DataGenerationTests(unittest.TestCase):
    def test_schema_and_satellites(self):
        df = simulate_dataset(samples_per_satellite=100)
        expected = {"satellite_id", "timestamp", "power_w", "temp_c", "voltage_v", "wheel_rpm", "fault_class"}
        self.assertTrue(expected.issubset(set(df.columns)))
        self.assertEqual(df["satellite_id"].nunique(), 10)


if __name__ == "__main__":
    unittest.main()
