## Create jump host . We will allow this jump host to access GKE cluster. the ip of this jump host is already authorized to allowin the GKE cluster
resource "google_compute_address" "my_internal_ip_addr" {
  project      = var.project
  address_type = "INTERNAL"
  region       = var.region
  subnetwork   = var.subnet
  name         = "my-ip1"
  address      = "10.0.0.7"
  description  = "An internal IP address for my jump host"
}

resource "google_compute_instance" "default" {
  project      = var.project
  zone         = var.zone
  name         = "jump-host"
  machine_type = "e2-medium"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network    = var.vpc
    subnetwork = var.subnet # Replace with a reference or self link to your subnet, in quotes
    network_ip = google_compute_address.my_internal_ip_addr.address
  }
}

## Creare Firewall to access jump hist via iap
resource "google_compute_firewall" "rules" {
  project = var.project
  name    = "allow-ssh"
  network = var.vpc # Replace with a reference or self link to your network, in quotes

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = ["35.235.240.0/20"]
}

## Create IAP SSH permissions for your jumphost instance
resource "google_project_iam_member" "project" {
  project = var.project
  role    = "roles/iap.tunnelResourceAccessor"
  member  = "serviceAccount:gcp-jrpdemo@gcp-demo-399901.iam.gserviceaccount.com"
}
