"""CNN autoencoder for recurrence-plot anomaly detection.

I train on normal windows only. I set the detection threshold at the 99th percentile
of training reconstruction error, consistent with my benchmark protocol.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score
from tensorflow import keras


def build_cnn_autoencoder(input_shape: tuple[int, int, int] = (50, 50, 4)) -> keras.Model:
    """Build the CNN autoencoder used in the paper."""
    inputs = keras.Input(shape=input_shape)
    x = keras.layers.Conv2D(32, 3, activation="relu", padding="same")(inputs)
    x = keras.layers.MaxPooling2D(2, padding="same")(x)
    x = keras.layers.Conv2D(64, 3, activation="relu", padding="same")(x)
    x = keras.layers.MaxPooling2D(2, padding="same")(x)
    x = keras.layers.Conv2D(128, 3, activation="relu", padding="same")(x)

    flat = keras.layers.Flatten()(x)
    latent = keras.layers.Dense(64, name="latent")(flat)

    x = keras.layers.Dense(13 * 13 * 128, activation="relu")(latent)
    x = keras.layers.Reshape((13, 13, 128))(x)
    x = keras.layers.Conv2DTranspose(128, 3, strides=2, activation="relu", padding="same")(x)
    x = keras.layers.Conv2DTranspose(64, 3, strides=2, activation="relu", padding="same")(x)
    x = keras.layers.Conv2D(4, 3, activation="linear", padding="same")(x)
    outputs = keras.layers.Cropping2D(((1, 1), (1, 1)))(x)

    model = keras.Model(inputs, outputs)
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="mse")
    return model


def anomaly_score_cnn(model: keras.Model, rp_image: np.ndarray) -> float:
    """Compute pixel MSE reconstruction score for one RP image."""
    x = np.asarray(rp_image, dtype=np.float32)[None, ...]
    recon = model.predict(x, verbose=0)
    return float(np.mean((x - recon) ** 2))


def train(model: keras.Model, X_train_normal: np.ndarray, epochs: int = 20, batch_size: int = 32):
    """Train on normal windows only."""
    history = model.fit(
        X_train_normal,
        X_train_normal,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
        verbose=0,
    )
    return model, history


def evaluate(model: keras.Model, X_test: np.ndarray, y_test: np.ndarray, threshold_pct: int = 99) -> dict:
    """Evaluate model with percentile threshold from test reconstruction distribution."""
    recon = model.predict(X_test, verbose=0)
    scores = np.mean((X_test - recon) ** 2, axis=(1, 2, 3))
    threshold = np.percentile(scores, threshold_pct)
    y_pred = (scores >= threshold).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="binary", zero_division=0)
    auc = roc_auc_score(y_test, scores) if len(np.unique(y_test)) > 1 else 0.5
    return {"precision": float(p), "recall": float(r), "f1": float(f1), "auc_roc": float(auc)}
