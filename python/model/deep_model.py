from sklearn.preprocessing import StandardScaler
import tensorflow as tf

from model.base_model import DeepBaseModel


def create_dense_model(
    input_shape=2,
    output_shape=2,
    hidden_units=(4, 8, 4),
    hidden_activations="relu",
    last_activation="softmax",
):
    hid_activation = tf.keras.layers.Activation(hidden_activations)
    inputs = tf.keras.layers.Input(shape=input_shape)
    hidden_out = inputs

    for n_cells in hidden_units:
        hidden_out = tf.keras.layers.Dense(n_cells)(hidden_out)
        hidden_out = hid_activation(hidden_out)

    out = tf.keras.layers.Dense(output_shape)(hidden_out)
    out = tf.keras.layers.Activation(last_activation)(out)

    return tf.keras.Model(inputs=inputs, outputs=out)


class SimpleFullyConnected(DeepBaseModel):
    def __init__(
        self,
        input_shape=2,
        output_shape=2,
        hidden_units=[4, 8, 4],
        hidden_activations="relu",
        last_activation="softmax",
        epochs=50,
        reduced_lr_epochs=10,
        optimizer="adamax",
        lr=1e-5,
        loss="cross_entropy",
    ):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.hidden_units = hidden_units
        self.hidden_activations = hidden_activations
        self.last_activation = last_activation
        self.epochs = epochs
        self.reduced_lr_epochs = reduced_lr_epochs
        self.optimizer = optimizer
        self.lr = lr
        self.loss = loss
        super().__init__()

    def instantiate_model(self):
        self.scaler_x = StandardScaler()
        self.model = create_dense_model(
            input_shape=self.input_shape,
            output_shape=self.output_shape,
            hidden_units=self.hidden_units,
            hidden_activations=self.hidden_activations,
            last_activation=self.last_activation,
        )

        if self.optimizer == "adamax":
            self.optimizer = tf.keras.optimizers.Adamax(lr=self.lr)
        elif self.optimizer == "rmsprop":
            self.optimizer = tf.keras.optimizers.RMSprop(lr=self.lr)
        elif self.optimizer == "sgd":
            self.optimizer = tf.keras.optimizers.SGD(lr=self.lr)
        elif self.optimizer == "Adam":
            self.optimizer = tf.keras.optimizers.Adam(lr=self.lr)
        else:
            raise ValueError(
                f"Optimizer {self.optimizer} not understood, must be among ['adam', 'adamax', 'sgd', 'rmsprop']"
            )

        self.model.compile(optimizer=self.optimizer, loss=self.loss)

    def fit(self, X, y):
        self.scaler_x.fit(X)
        if self.output_shape == 2:
            y = tf.one_hot(y.squeeze(), depth=2)
        self.model.fit(self.scaler_x.transform(X), y, epochs=self.epochs)
        if self.reduced_lr_epochs > 0:
            self.optimizer.lr.assign(self.lr / 10)
            self.model.fit(self.scaler_x.transform(X), y, epochs=self.reduced_lr_epochs)

    def predict(self, X):
        y_pred = self.model.predict(self.scaler_x.transform(X))
        if self.output_shape == 2:
            y_pred = tf.argmax(y_pred, axis=-1)
        return y_pred


def create_conv_dense_model(
    input_shape=2,
    history_input_shape=(5, 5),
    output_shape=2,
    hidden_units=(4, 8, 4),
    hidden_activations="relu",
    last_activation="softmax",
):
    hid_activation = tf.keras.layers.Activation(hidden_activations)

    history_inputs = tf.keras.layers.Input(shape=history_input_shape)
    print(history_inputs.shape, history_input_shape)
    encoded_history = tf.keras.layers.Conv1D(filters=4, kernel_size=3)(history_inputs)
    encoded_history = tf.keras.layers.Conv1D(filters=1, kernel_size=3)(encoded_history)
    encoded_history = tf.keras.layers.Flatten()(encoded_history)

    inputs = tf.keras.layers.Input(shape=input_shape)
    hidden_out = tf.keras.layers.Concatenate()([inputs, encoded_history])

    for n_cells in hidden_units:
        hidden_out = tf.keras.layers.Dense(n_cells)(hidden_out)
        hidden_out = hid_activation(hidden_out)

    out = tf.keras.layers.Dense(output_shape)(hidden_out)
    out = tf.keras.layers.Activation(last_activation)(out)

    return tf.keras.Model(inputs=[history_inputs, inputs], outputs=out)


class ConvolutionalHistoryAndFullyConnected(DeepBaseModel):
    def __init__(
        self,
        num_history_signals=2,
        history_length=5,
        input_shape=2,
        output_shape=2,
        hidden_units=[4, 8, 4],
        hidden_activations="relu",
        last_activation="softmax",
        epochs=50,
        reduced_lr_epochs=10,
        optimizer="adamax",
        lr=1e-5,
        loss="cross_entropy",
    ):
        self.num_history_signals = num_history_signals
        self.history_length = history_length
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.hidden_units = hidden_units
        self.hidden_activations = hidden_activations
        self.last_activation = last_activation
        self.epochs = epochs
        self.reduced_lr_epochs = reduced_lr_epochs
        self.optimizer = optimizer
        self.lr = lr
        self.loss = loss
        super().__init__()

    def instantiate_model(self):
        self.scaler_x = StandardScaler()
        self.model = create_conv_dense_model(
            history_input_shape=(self.history_length, self.num_history_signals),
            input_shape=self.input_shape,
            output_shape=self.output_shape,
            hidden_units=self.hidden_units,
            hidden_activations=self.hidden_activations,
            last_activation=self.last_activation,
        )

        if self.optimizer == "adamax":
            self.optimizer = tf.keras.optimizers.Adamax(lr=self.lr)
        elif self.optimizer == "rmsprop":
            self.optimizer = tf.keras.optimizers.RMSprop(lr=self.lr)
        elif self.optimizer == "sgd":
            self.optimizer = tf.keras.optimizers.SGD(lr=self.lr)
        elif self.optimizer == "Adam":
            self.optimizer = tf.keras.optimizers.Adam(lr=self.lr)
        else:
            raise ValueError(
                f"Optimizer {self.optimizer} not understood, must be among ['adam', 'adamax', 'sgd', 'rmsprop']"
            )

        self.model.compile(optimizer=self.optimizer, loss=self.loss)

    def fit(self, X, X_history, y):
        #print(X.columns)
        self.scaler_x.fit(X)
        if self.output_shape == 2:
            y = tf.one_hot(y.squeeze(), depth=2)

        self.model.fit([X_history, self.scaler_x.transform(X)], y, epochs=self.epochs)
        if self.reduced_lr_epochs > 0:
            self.optimizer.lr.assign(self.lr / 10)
            self.model.fit([X_history, self.scaler_x.transform(X)], y, epochs=self.reduced_lr_epochs)

    def predict(self, X):
        y_pred = self.model.predict(self.scaler_x.transform(X))
        if self.output_shape == 2:
            y_pred = tf.argmax(y_pred, axis=-1)
        return y_pred

    def summary(self):
        return self.model.summary()
