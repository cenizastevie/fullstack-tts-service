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

output "ecr_repository_url" {
  value       = aws_ecr_repository.fastapi.repository_url
  description = "The URL of the ECR repository"
}