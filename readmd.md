Google Cloud Compute Engine is a powerful infrastructure service that allows users to run virtual machines on Google's global infrastructure. It provides flexible and scalable compute resources with various machine types and options tailored to different workloads.
This document outlines alternative deployment methods for GCP Vertex AI products  when Terraform is not supported.

Harness is a modern DevOps platform that automates the deployment of applications, infrastructure, and cloud resources. It simplifies Continuous Integration (CI), Continuous Delivery (CD), and Continuous Deployment (CD) workflows. When deploying Google Cloud Platform (GCP) resources, Harness can integrate with Python client libraries to execute scripts that automate resource provisioning and management.

Prerequisites
Harness Access

Ensure you have access to the Harness platform with appropriate permissions to create and manage pipelines.
Repository Access

Access to the Git repository where the Python code for deploying GCP resources is stored. This code will typically:
Authenticate with GCP using OIDC or a service account.
Use GCP Python client libraries (e.g., google-cloud-storage, google-cloud-aiplatform, etc.) to provision resources.
OIDC Setup for Authentication

Set up OIDC authentication between Harness and GCP to allow Harness pipelines to authenticate and interact with GCP securely. Follow the official documentation for detailed steps, which generally include:
Creating a Google Cloud service account with necessary permissions.
Configuring an OIDC identity provider in GCP.
Setting up Harness to authenticate with GCP using OIDC.
Provisioning Service Account

The GCP service account must have the necessary permissions to deploy and manage the required resources. This may include roles like:
roles/iam.serviceAccountUser
roles/storage.admin (for Cloud Storage)
roles/aiplatform.admin (for Vertex AI resources)
roles/compute.admin (for Compute Engine)

Managing machine learning models involves challenges like versioning, deployment, governance, collaboration, and scalability. Vertex AI Model Registry addresses these by providing a centralized repository to store, version, and track models with metadata. It ensures compliance through lineage tracking, enhances collaboration with controlled access, and integrates seamlessly with Vertex AI workflows to simplify model management and deployment.
