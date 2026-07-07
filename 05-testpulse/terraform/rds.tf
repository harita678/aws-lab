# ============================================================================
# rds.tf — RDS Instance on AWS
# ============================================================================


resource "aws_db_instance" "testpulse_db" {

  lifecycle {
    prevent_destroy = true
  }

  identifier        = "harita-testpulse-db"
  engine            = "postgres"
  engine_version    = "18.3"
  instance_class    = "db.t4g.micro"
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = var.DB_NAME
  username = var.DB_USERNAME
  port     = var.DB_PORT
  password = var.DB_PASSWORD

  multi_az            = false
  publicly_accessible = false

  vpc_security_group_ids = [aws_security_group.db.id]

  db_subnet_group_name = "default-vpc-0195a8984f6090bc2"

  storage_encrypted = true

  skip_final_snapshot = true
  copy_tags_to_snapshot = true
  max_allocated_storage = 1000

}