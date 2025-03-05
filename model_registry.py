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


from google.cloud import aiplatform_v1

def import_model_version(
    project: str,
    location: str,
    model_display_name: str,
    kms_key_name: str,
    container_image_uri: str,
    artifact_uri: str,
):
    """
    Imports a new version of a model to Vertex AI Model Registry.

    Args:
        project: Google Cloud project ID.
        location: Location where the model is stored (e.g., "us-central1").
        model_display_name: The display name of the existing model.
        kms_key_name: The KMS key to encrypt the model.
        container_image_uri: The container image URI for serving the model.
        artifact_uri: The GCS path to the model artifacts.
    """
    client = aiplatform_v1.ModelServiceClient()

    # Define the parent resource path for the model
    parent = f"projects/{project}/locations/{location}"

    # Configure the model version to upload
    model = {
        "display_name": model_display_name,
        "artifact_uri": artifact_uri,
        "encryption_spec": {"kms_key_name": kms_key_name},
        "container_spec": {
            "image_uri": container_image_uri,
        },
    }

    # Upload the new version
    operation = client.upload_model(parent=parent, model=model)

    print("Uploading model version... This may take a while.")
    response = operation.result()
    print("Model version imported successfully.")
    print(f"Model resource name: {response.model}")


if __name__ == "__main__":
    # User-defined variables
    PROJECT_ID = "your-project-id"  # Replace with your project ID
    LOCATION = "us-central1"  # Replace with your preferred location
    MODEL_DISPLAY_NAME = "your-model-display-name"  # Replace with your model display name
    KMS_KEY_NAME = "ajkk"  # Replace with your KMS key name
    CONTAINER_IMAGE_URI = "bsk"  # Replace with your container image URI
    ARTIFACT_URI = "gs://skb"  # Replace with your GCS artifact URI

    import_model_version(
        project=PROJECT_ID,
        location=LOCATION,
        model_display_name=MODEL_DISPLAY_NAME,
        kms_key_name=KMS_KEY_NAME,
        container_image_uri=CONTAINER_IMAGE_URI,
        artifact_uri=ARTIFACT_URI,
    )



from google.cloud import aiplatform_v1
from google.protobuf import field_mask_pb2

def update_model_mask(project_id: str, location: str, model_id: str, update_mask_paths: list):
    # Initialize the ModelServiceClient
    client = aiplatform_v1.ModelServiceClient(client_options={
        "api_endpoint": f"{location}-aiplatform.googleapis.com"
    })

    # Construct the fully qualified model name
    model_name = client.model_path(project=project_id, location=location, model=model_id)

    # Create a FieldMask object with the paths to update
    field_mask = field_mask_pb2.FieldMask(paths=update_mask_paths)

    # Create a Model object with the fields to update
    # For example, updating the display name and labels
    model = aiplatform_v1.Model(
        name=model_name,
        display_name="New Display Name",  # Example field to update
        labels={"new_label": "new_value"}  # Example field to update
    )

    # Update the model with the specified mask
    updated_model = client.update_model(model=model, update_mask=field_mask)

    print("Model updated successfully:")
    print(updated_model)

# Example usage
project_id = "your-project-id"
location = "us-central1"
model_id = "your-model-id"
update_mask_paths = ["display_name", "labels"]  # Specify the fields to update

update_model_mask(project_id, location, model_id, update_mask_paths)


