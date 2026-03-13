"""LSTM autoencoder baseline for telemetry sequence anomalies."""

from tensorflow import keras


def build_lstm_autoencoder(timesteps=64, features=4):
    inputs = keras.Input(shape=(timesteps, features))
    encoded = keras.layers.LSTM(32, activation="tanh")(inputs)
    repeated = keras.layers.RepeatVector(timesteps)(encoded)
    decoded = keras.layers.LSTM(32, return_sequences=True)(repeated)
    outputs = keras.layers.TimeDistributed(keras.layers.Dense(features))(decoded)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="mse")
    return model
