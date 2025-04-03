import json
import subprocess

# Set variables
BUCKET_NAME = "your-bucket-name"
FOLDER_PATH = "your-batch-output-folder/"
SERVICE_ACCOUNT_KEY = "path-to-your-service-account.json"

# Authenticate using service account
subprocess.run([
    "gcloud", "auth", "activate-service-account", "--key-file", SERVICE_ACCOUNT_KEY
], check=True)

# Get list of files in the output folder
list_cmd = [
    "curl", "-X", "GET", 
    f"https://storage.googleapis.com/storage/v1/b/{BUCKET_NAME}/o?prefix={FOLDER_PATH}",
    "-H", "Authorization: Bearer $(gcloud auth print-access-token)"
]

result = subprocess.run(list_cmd, capture_output=True, text=True)
file_list = json.loads(result.stdout)

# Extract file names
files = [item["name"] for item in file_list.get("items", [])]

# Download each file
for file_name in files:
    download_cmd = [
        "curl", "-X", "GET", 
        f"https://storage.googleapis.com/storage/v1/b/{BUCKET_NAME}/o/{file_name}?alt=media",
        "-H", "Authorization: Bearer $(gcloud auth print-access-token)"
    ]
    output_file = file_name.split("/")[-1]  # Extract just the file name
    with open(output_file, "wb") as f:
        subprocess.run(download_cmd, stdout=f, check=True)
    print(f"Downloaded {output_file}")
