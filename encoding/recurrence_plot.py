"""Recurrence plot utilities.

I encode univariate telemetry windows as recurrence images based on pairwise distances.
This follows the recurrence plot concept from Eckmann, Kamphorst, and Ruelle (1987).
I use the encoded images as model inputs, consistent with Wang and Oates (2015).
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def window_to_rp_image(window: np.ndarray, eps: float = 0.1) -> np.ndarray:
    """Convert a 1D window into a binary recurrence image."""
    arr = np.asarray(window, dtype=np.float32).reshape(-1, 1)
    distances = np.sqrt((arr - arr.T) ** 2)
    return (distances <= eps).astype(np.float32)


def batch_encode(windows: np.ndarray, eps: float = 0.1, verbose: bool = True) -> np.ndarray:
    """Vectorized recurrence encoding for a batch of windows.

    Expected input shape is (n_windows, window_len).
    """
    windows = np.asarray(windows, dtype=np.float32)
    iterator = tqdm(windows, disable=not verbose, desc="Encoding RP")
    images = [window_to_rp_image(w, eps=eps) for w in iterator]
    return np.stack(images, axis=0)


def visualize_rp(rp_image: np.ndarray, title: str | None = None) -> None:
    """Display a recurrence plot image."""
    plt.figure(figsize=(4, 4))
    plt.imshow(rp_image, cmap="binary", vmin=0, vmax=1)
    plt.xlabel("t")
    plt.ylabel("t")
    plt.title(title or "Recurrence plot")
    plt.tight_layout()
    plt.show()
