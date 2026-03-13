import unittest

import numpy as np

from evaluation.compute_metrics import compute_overall_metrics


class MetricTests(unittest.TestCase):
    def test_metric_keys(self):
        y_true = np.array([0, 1, 0, 1, 1])
        y_score = np.array([0.1, 0.9, 0.3, 0.8, 0.7])
        metrics = compute_overall_metrics(y_true, y_score)
        for key in ["precision", "recall", "f1", "auc_roc"]:
            self.assertIn(key, metrics)


if __name__ == "__main__":
    unittest.main()
