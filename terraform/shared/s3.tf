# S3 Bucket
resource "aws_s3_bucket" "medical_images" {
  bucket = "${var.bucket_name_prefix}-${var.environment}-medical-images"

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-medical-images"
    Environment = var.environment
  }
}

# Versioning Configuration
resource "aws_s3_bucket_versioning" "medical_images_versioning" {
  bucket = aws_s3_bucket.medical_images.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Server-Side Encryption Configuration
resource "aws_s3_bucket_server_side_encryption_configuration" "medical_images_encryption" {
  bucket = aws_s3_bucket.medical_images.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
