resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-db"
  subnet_ids = var.db_subnet_ids
}

resource "aws_db_instance" "postgres" {
  identifier             = "${var.name}-postgres"
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  storage_encrypted      = true
  db_name                = "telemed"
  username               = "telemed"
  password               = "CHANGE-ME-IN-REAL-DEPLOYMENT"
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [var.db_sg_id]
  publicly_accessible    = false
  skip_final_snapshot    = true
}
