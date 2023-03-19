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

    def __init__(self,
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
        self.model = create_dense_model(input_shape=self.input_shape,
                                        output_shape=self.output_shape,
                                        hidden_units=self.hidden_units,
                                        hidden_activations=self.hidden_activations,
                                        last_activation=self.last_activation)

        if self.optimizer == "adamax":
            self.optimizer = tf.keras.optimizers.Adamax(lr=self.lr)
        elif self.optimizer == "rmsprop":
            self.optimizer = tf.keras.optimizers.RMSprop(lr=self.lr)
        elif self.optimizer == "sgd":
            self.optimizer = tf.keras.optimizers.SGD(lr=self.lr)
        elif self.optimizer == "Adam":
            self.optimizer = tf.keras.optimizers.Adam(lr=self.lr)
        else:
            raise ValueError(f"Optimizer {self.optimizer} not understood, must be among ['adam', 'adamax', 'sgd', 'rmsprop']")

        self.model.compile(optimizer=self.optimizer, loss=self.loss)

    def fit(self, X, y):
        if self.output_shape == 2:
            y = tf.one_hot(y.squeeze(), depth=2)
        self.model.fit(X, y, epochs=self.epochs)
        if self.reduced_lr_epochs > 0:
            self.optimizer.lr.assign(self.lr / 10)
            self.model.fit(X, y, epochs=self.reduced_lr_epochs)

    def predict(self, X):
        return self.model.predict(X)
