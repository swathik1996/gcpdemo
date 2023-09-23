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

variable "tag" {
    type = string
    description = "tag"
}

