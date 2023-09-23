
# create cloud router for nat gateway
resource "google_compute_router" "router" {
  project = var.project
  name    = var.routername
  network = var.vpc
  region  = var.region
}

## Create Nat Gateway with module
module "cloud-nat" {
  source     = "terraform-google-modules/cloud-nat/google"
  version    = "~> 1.2"
  project_id = var.project
  region     = var.region
  router     = google_compute_router.router.name
  name       = var.natname
}
