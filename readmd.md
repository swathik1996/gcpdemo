Google Cloud Compute Engine is a powerful infrastructure service that allows users to run virtual machines on Google's global infrastructure. It provides flexible and scalable compute resources with various machine types and options tailored to different workloads.
This document outlines alternative deployment methods for GCP Vertex AI products  when Terraform is not supported.

Products Not Supported by Terraform
While Terraform is a powerful tool for infrastructure management, it doesn't cover all Vertex AI functionalities. Here are alternative approaches:

gcloud Command-Line Interface (CLI): Google Cloud provides a command-line tool called gcloud for interacting with various services, including Vertex AI. These commands offer granular control over deployments. Refer to the official documentation for specific commands: https://cloud.google.com/sdk/gcloud/reference/ai-platform
REST API: Vertex AI exposes a RESTful API for programmatic interactions. It allows sending HTTP requests to specific endpoints to manage Vertex AI resources. Detailed API reference can be found here: https://cloud.google.com/vertex-ai/docs/general/deployment
Python Client Libraries: Google offers client libraries for various programming languages, including Python. These libraries simplify interacting with the Vertex AI API from your code. Refer to the Python client library documentation: https://pypi.org/project/google-cloud-aiplatform/
Choosing the Right Approach
Here's a quick breakdown to help you choose the most suitable method:

REST API:

Pros:
Offers the most flexibility and control.
Integrates well with custom applications.
Cons:
Requires coding knowledge and understanding of the API structure.
Manual error handling and authentication setup are needed.
Terracurl (Not Recommended for Vertex AI Model Garden)
While Terraform provides infrastructure as code (IaC) management, Terracurl aims to offer a similar approach for APIs. However, it's currently not recommended for deploying Vertex AI Model Garden resources due to potential issues encountered in the past.

Alternatives to Terracurl for Vertex AI:

gcloud CLI: Provides a user-friendly interface for deployment tasks.
REST API: Offers granular control and can be integrated with automation tools.
For deploying Vertex AI models, using gcloud or the REST API directly is generally preferred over Terracurl at this time.

This document aims to provide a starting point for exploring non-Terraform deployment options for your GCP Vertex AI projects. Choose the approach that best aligns with your technical expertise and project requirements.

Here’s an overview of deploying resources on GCP using REST APIs with Terraform-based approaches:

a) REST API Terraform Provider
This method involves using the Mastercard REST API provider to interact with REST endpoints as part of a Terraform configuration.

Explanation
The restapi_object resource allows you to create, update, and delete objects via REST API calls directly within your Terraform configuration. You define the REST endpoint, request headers, and the request body, enabling Terraform to manage resources that don’t have official Terraform providers.

Example Workflow
Define REST API Object in Terraform:

hcl
Copy code
provider "restapi" {
  uri    = "https://api.example.com"
  headers = {
    Authorization = "Bearer <TOKEN>"
    Content-Type  = "application/json"
  }
}

resource "restapi_object" "example" {
  path         = "/v1/resource"
  method       = "POST"
  data         = jsonencode({
    name  = "example"
    value = "data"
  })
  search_key   = "id"
}
Deploy using Terraform as you would with any other resource:

bash
Copy code
terraform init
terraform apply
Pros
Minimal changes in workflow: Seamlessly integrates with Terraform, allowing you to manage all resources from a single configuration.
Flexibility: Can be used to manage any REST API-based resource, even if a dedicated Terraform provider doesn’t exist.
Cons
Yet to be tested or used in DAII: May require validation in your specific deployment environment for compatibility with internal workflows.
Limited error handling: Compared to official Terraform providers, error handling might need custom scripts or manual intervention.
b) TerraCurl
TerraCurl is a lightweight provider that enables you to run curl commands inside Terraform to interact with REST APIs.

Explanation
It is essentially a wrapper around the curl command, making API requests directly from within Terraform configurations. This approach is useful for quick, lightweight API interactions but isn’t ideal for complex resource management.

Example Workflow
Define API call in Terraform:

hcl
Copy code
provider "terracurl" {}

resource "terracurl_curl" "example" {
  command = "curl -X POST -H 'Authorization: Bearer <TOKEN>' -H 'Content-Type: application/json' -d '{\"name\": \"example\"}' https://api.example.com/v1/resource"
}
Deploy using Terraform:

bash
Copy code
terraform init
terraform apply
Pros
Quick setup: No need to configure complex providers or resources.
Lightweight: Ideal for small, quick API calls.
Cons
Not a recommended approach: It’s more of a workaround than a solution for production environments.
Limited Terraform integration: Doesn’t maintain state in the same way as official providers, making it difficult to track resource changes.
No native Terraform lifecycle management: curl commands aren’t natively managed by Terraform’s lifecycle, so state drift can occur.
