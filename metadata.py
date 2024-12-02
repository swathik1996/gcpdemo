from google.api_core.operation import Operation
from google.cloud import aiplatform_v1

def create_metadata_store(project_id, location, metadata_store_id, kms_key_name):
   # Define the API endpoint based on the location
    api_endpoint = f"{location}-aiplatform.googleapis.com"

    # Initialize the client with the specified API endpoint
    client = aiplatform_v1.MetadataServiceClient(client_options={"api_endpoint": api_endpoint})
    parent=f"projects/{project_id}/locations/{location}"

    encryption_spec = aiplatform_v1.EncryptionSpec(kms_key_name=kms_key_name)
    metadata_store = aiplatform_v1.MetadataStore(encryption_spec=encryption_spec)

    # Initialize request argument(s)
    request = aiplatform_v1.CreateMetadataStoreRequest(
        parent=parent,
        metadata_store=metadata_store,
        metadata_store_id=metadata_store_id
    )

    # Make the request
    operation = client.create_metadata_store(request=request)

    print("Creating metadata store")

    response = operation.result()

    # Handle the response
    print(response)

project_id = "burner-swakirub"
location = "us-central1"
metadata_store_id = "default"
kms_key_name = "projects/burner-swakirub/locations/us-central1/keyRings/metadata/cryptoKeys/vertex_ai"

#create_metadata_store(project_id, location, metadata_store_id, kms_key_name)


def delete_metadata_store():
    api_endpoint = f"{location}-aiplatform.googleapis.com"
    client = aiplatform_v1.MetadataServiceClient(client_options={"api_endpoint": api_endpoint})
    request = aiplatform_v1.DeleteMetadataStoreRequest(
        name=f"projects/629388689028/locations/us-central1/metadataStores/default",
    )
    # Make the request
    operation = client.delete_metadata_store(request=request)
    print("Deleting metadata store")
    response = operation.result()
    # Handle the response
    print(response)


delete_metadata_store()
