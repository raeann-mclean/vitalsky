variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "cloud-telemedicine"
}

variable "environment" {
  type    = string
  default = "demo"
}

variable "db_instance_class" {
  type    = string
  default = "db.t4g.micro"
}
