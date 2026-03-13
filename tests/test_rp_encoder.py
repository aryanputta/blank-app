import unittest

import numpy as np

from recurrence_plot_encoder.rp_encoder import telemetry_to_rp


class RPEncoderTests(unittest.TestCase):
    def test_tensor_shape(self):
        window = np.random.default_rng(0).normal(size=(50, 4)).astype("float32")
        tensor = telemetry_to_rp(window, eps=0.1)
        self.assertEqual(tensor.shape, (50, 50, 4))


if __name__ == "__main__":
    unittest.main()
