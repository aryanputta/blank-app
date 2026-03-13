"""LSTM autoencoder for telemetry sequence anomaly detection.

I train only on normal windows and use a fixed threshold at the 99th percentile
of reconstruction error.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score
from tensorflow import keras


def build_lstm_autoencoder(input_shape: tuple[int, int] = (50, 4)) -> keras.Model:
    """Build LSTM encoder-decoder model."""
    inputs = keras.Input(shape=input_shape)
    x = keras.layers.LSTM(128)(inputs)
    x = keras.layers.RepeatVector(input_shape[0])(x)
    x = keras.layers.LSTM(128, return_sequences=True)(x)
    outputs = keras.layers.TimeDistributed(keras.layers.Dense(input_shape[1]))(x)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="mse")
    return model


def anomaly_score_lstm(model: keras.Model, seq_window: np.ndarray) -> float:
    """Compute reconstruction MSE score for one sequence window."""
    x = np.asarray(seq_window, dtype=np.float32)[None, ...]
    recon = model.predict(x, verbose=0)
    return float(np.mean((x - recon) ** 2))


def train(model: keras.Model, X_train_normal: np.ndarray, epochs: int = 20, batch_size: int = 32):
    """Train LSTM autoencoder on normal windows."""
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
    """Evaluate with percentile threshold on reconstruction error."""
    recon = model.predict(X_test, verbose=0)
    scores = np.mean((X_test - recon) ** 2, axis=(1, 2))
    threshold = np.percentile(scores, threshold_pct)
    y_pred = (scores >= threshold).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="binary", zero_division=0)
    auc = roc_auc_score(y_test, scores) if len(np.unique(y_test)) > 1 else 0.5
    return {"precision": float(p), "recall": float(r), "f1": float(f1), "auc_roc": float(auc)}
