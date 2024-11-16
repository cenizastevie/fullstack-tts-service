resource "aws_db_instance" "medical_db" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-medical-db"
    Environment = var.environment
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.bucket_name_prefix}-${var.environment}-db-subnet-group"
  subnet_ids = [aws_subnet.main_a.id, aws_subnet.main_b.id]

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-db-subnet-group"
    Environment = var.environment
  }
}