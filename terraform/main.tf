locals {
  name = "${var.project_name}-${var.environment}"
}

module "vpc" {
  source = "./modules/vpc"

  name = local.name
}

module "security" {
  source = "./modules/security"

  name   = local.name
  vpc_id = module.vpc.vpc_id
}

module "rds" {
  source = "./modules/rds"

  name              = local.name
  db_subnet_ids     = module.vpc.db_subnet_ids
  db_sg_id          = module.security.db_sg_id
  db_instance_class = var.db_instance_class
}

module "ecs" {
  source = "./modules/ecs"

  name               = local.name
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  api_sg_id          = module.security.api_sg_id
}

module "messaging" {
  source = "./modules/messaging"

  name = local.name
}

module "storage" {
  source = "./modules/storage"

  name = local.name
}
