resource "aws_ecr_repository" "fastapi" {
  name = "${var.bucket_name_prefix}-${var.environment}-repository"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-repository"
    Environment = var.environment
  }
}
