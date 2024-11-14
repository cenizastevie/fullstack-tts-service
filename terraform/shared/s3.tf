resource "aws_s3_bucket" "audio" {
  bucket = "${var.bucket_name_prefix}-${var.environment}-audio"

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-audio"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "pdf" {
  bucket = "${var.bucket_name_prefix}-${var.environment}-pdf"

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-pdf"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "text" {
  bucket = "${var.bucket_name_prefix}-${var.environment}-text"

  tags = {
    Name        = "${var.bucket_name_prefix}-${var.environment}-text"
    Environment = var.environment
  }
}