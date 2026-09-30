variable "name" { type = string }

# Networking inputs for the ECS service (wired from the root module; not used by any resource yet)
variable "vpc_id" { type = string }
variable "private_subnet_ids" { type = list(string) }
variable "api_sg_id" { type = string }
