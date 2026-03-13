import unittest

from evaluation.evaluate_models import TEST_SATELLITES, TRAIN_SATELLITES


class SplitTests(unittest.TestCase):
    def test_no_overlap(self):
        self.assertTrue(set(TRAIN_SATELLITES).isdisjoint(set(TEST_SATELLITES)))


if __name__ == "__main__":
    unittest.main()
