import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
import mlflow
import mlflow.tensorflow

# Set the tracking URI to local file system
mlflow.set_tracking_uri("file:///tmp/mlruns")
mlflow.set_experiment("TensorFlow Demo")

# Load the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize the data
x_train, x_test = x_train / 255.0, x_test / 255.0

# Create a simple neural network model
class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(32, 3, activation='relu')
        self.flatten = Flatten()
        self.d1 = Dense(128, activation='relu')
        self.d2 = Dense(10, activation='softmax')

    def call(self, x):
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)

model = MyModel()

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Define the training process within an MLflow run
with mlflow.start_run():
    # Log model summary
    model.summary()

    # Log hyperparameters
    mlflow.log_param("optimizer", "adam")
    mlflow.log_param("loss_function", "sparse_categorical_crossentropy")
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("epochs", 5)

    # Train the model
    history = model.fit(x_train, y_train, epochs=5, batch_size=32, validation_data=(x_test, y_test))

    # Log metrics
    for epoch in range(5):
        mlflow.log_metric("train_loss", history.history['loss'][epoch], step=epoch)
        mlflow.log_metric("train_accuracy", history.history['accuracy'][epoch], step=epoch)
        mlflow.log_metric("val_loss", history.history['val_loss'][epoch], step=epoch)
        mlflow.log_metric("val_accuracy", history.history['val_accuracy'][epoch], step=epoch)

    # Log the model
    mlflow.tensorflow.log_model(model, "model")
