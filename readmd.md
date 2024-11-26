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
