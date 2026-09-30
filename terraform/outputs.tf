output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnets" {
  value = module.vpc.private_subnet_ids
}

output "database_endpoint" {
  value     = module.rds.database_endpoint
  sensitive = true
}

output "ecr_repository" {
  value = module.ecs.ecr_repository
}
