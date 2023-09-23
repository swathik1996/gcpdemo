
# Create GKE cluster with 2 nodes in our custom VPC/Subnet
resource "google_container_cluster" "primary" {
  name                     = var.clustername
  location                 = var.zone
  network                  = var.vpc
  subnetwork               = var.subnet
  remove_default_node_pool = true ## create the smallest possible default node pool and immediately delete it.
  # networking_mode          = "VPC_NATIVE" 
  initial_node_count = 1

  private_cluster_config {
    enable_private_endpoint = true
    enable_private_nodes    = true
    master_ipv4_cidr_block  = var.mastercidr
  }
  ip_allocation_policy {
    cluster_ipv4_cidr_block  = var.clustercidr
    services_ipv4_cidr_block = var.servicecidr
  }
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.authorizedcidr
      display_name = "net1"
    }

  }
}

# Create managed node pool
resource "google_container_node_pool" "primary_nodes" {
  name       = google_container_cluster.primary.name
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]

    labels = {
      env = "dev"
    }

    machine_type = "n1-standard-1"
    preemptible  = true
    #service_account = google_service_account.mysa.email

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}


############Output############################################
output "kubernetes_cluster_host" {
  value       = google_container_cluster.primary.endpoint
  description = "GKE Cluster Host"
}

output "kubernetes_cluster_name" {
  value       = google_container_cluster.primary.name
  description = "GKE Cluster Name"
}