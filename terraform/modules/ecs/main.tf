resource "aws_ecr_repository" "api" {
  name                 = "${var.name}-api"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/${var.name}/api"
  retention_in_days = 14
}
