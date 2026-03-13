"""Dense autoencoder baseline for tabular telemetry windows."""

from tensorflow import keras


def build_autoencoder(input_dim=256):
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(input_dim,)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(32, activation="relu"),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(input_dim),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    return model
