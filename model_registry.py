import tensorflow as tf
import os

# Create a simple TPU-compatible model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(128,)),  # Example input shape
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')  # Binary classification output
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Save the model as a TensorFlow SavedModel
def save_model():
    model = create_model()

    # Define path for the model artifact
    artifact_path = "./tpu_dummy_model"
    os.makedirs(artifact_path, exist_ok=True)

    # Save the model in the SavedModel format
    model.save(artifact_path)
    print(f"Model artifact saved to: {artifact_path}")

if __name__ == "__main__":
    save_model()

gsutil cp -r ./tpu_dummy_model gs://your-bucket-name/path-to-tpu-dummy-model/
