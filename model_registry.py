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


from google.cloud import aiplatform

def import_model_version(
    model_id: str,
    project: str,
    location: str,
    kms_key_name: str,
    container_image_uri: str,
    artifact_uri: str,
):
    """
    Imports a new version of a model to Vertex AI Model Registry.

    Args:
        model_id: The ID of the existing model.
        project: Google Cloud project ID.
        location: Location where the model is stored (e.g., "us-central1").
        kms_key_name: The KMS key to encrypt the model.
        container_image_uri: The container image URI for serving the model.
        artifact_uri: The GCS path to the model artifacts.
    """
    # Initialize Vertex AI SDK
    aiplatform.init(project=project, location=location)

    # Construct the parent resource name
    parent = f"projects/{project}/locations/{location}/models/{model_id}"

    # Import the new version using ModelServiceClient
    from google.cloud.aiplatform_v1 import ModelServiceClient
    from google.cloud.aiplatform_v1.types import ImportModelRequest

    client = ModelServiceClient()

    request = ImportModelRequest(
        parent=parent,
        model={
            "artifact_uri": artifact_uri,
            "encryption_spec": {"kms_key_name": kms_key_name},
            "container_spec": {
                "image_uri": container_image_uri,
            },
        },
    )

    response = client.import_model(request=request)

    print("New version imported successfully.")
    print(f"Model version resource name: {response.name}")


if __name__ == "__main__":
    # User-defined variables
    MODEL_ID = "your-model-id"  # Replace with your model ID
    PROJECT_ID = "your-project-id"  # Replace with your project ID
    LOCATION = "us-central1"  # Replace with your preferred location
    KMS_KEY_NAME = "ajkk"  # Replace with your KMS key name
    CONTAINER_IMAGE_URI = "bsk"  # Replace with your container image URI
    ARTIFACT_URI = "gs://skb"  # Replace with your GCS artifact URI

    import_model_version(
        model_id=MODEL_ID,
        project=PROJECT_ID,
        location=LOCATION,
        kms_key_name=KMS_KEY_NAME,
        container_image_uri=CONTAINER_IMAGE_URI,
        artifact_uri=ARTIFACT_URI,
    )

