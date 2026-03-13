"""CNN model for recurrence plot anomaly detection."""

from tensorflow import keras


def build_cnn(input_shape=(64, 64, 1)):
    model = keras.Sequential(
        [
            keras.layers.Input(shape=input_shape),
            keras.layers.Conv2D(16, 3, activation="relu", padding="same"),
            keras.layers.MaxPool2D(),
            keras.layers.Conv2D(32, 3, activation="relu", padding="same"),
            keras.layers.GlobalAveragePooling2D(),
            keras.layers.Dense(32, activation="relu"),
            keras.layers.Dense(5, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model
