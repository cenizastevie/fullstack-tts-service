resource "aws_s3_bucket" "medical_images" {
  bucket = "${var.bucket_name_prefix}-${var.environment}-medical-images"

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-medical-images"
    Environment = var.environment
  }

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}