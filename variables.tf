variable "project" {
    type = string
    description = "Name of the Project"
}

variable "region" {
    type = string
    description = "Name of the Region"
}

variable "zone" {
    type = string
    description = "Name of the Zone"
}

variable "vpc" {
    type = string
    description = "Name of the VPC"
}

variable "subnet" {
    type = string
    description = "Name of the Subnet"
}

variable "networkcidr" {
  type = string
  description = "CIDR Range"
}

variable "natname" {
    type = string
    description = "Name of the NAT"
}

variable "routername" {
    type = string
    description = "Name of the Router"
}

variable "clustername" {
    type = string
    description = "Name of the Cluster"
}

variable "mastercidr" {
  type = string
  description = "Master CIDR Range"
}

variable "clustercidr" {
  type = string
  description = "Cluster nodes CIDR Range"
}

variable "servicecidr" {
  type = string
  description = "Service CIDR Range"
}

variable "authorizedcidr" {
  type = string
  description = "Jump server authorized CIDR Range"
}

variable "nodepoolmctype" {
    type = string
    description = "Name of the machine type"
}

variable "tag" {
    type = string
    description = "tag"
}