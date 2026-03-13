import unittest


class ModelIOTests(unittest.TestCase):
    def test_model_files_exist(self):
        import pathlib

        required = [
            pathlib.Path("models/cnn_autoencoder.py"),
            pathlib.Path("models/lstm_autoencoder.py"),
            pathlib.Path("models/standard_autoencoder.py"),
            pathlib.Path("models/isolation_forest.py"),
        ]
        for path in required:
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
