provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test" # LocalStack default access key
  secret_key                  = "test" # LocalStack default secret key
  skip_credentials_validation = var.dev_mode
  skip_metadata_api_check     = var.dev_mode
  skip_requesting_account_id  = var.dev_mode
  s3_use_path_style           = var.dev_mode

  endpoints {
    s3 = var.s3_endpoint # LocalStack S3 endpoint, usually "http://localhost:4566"
  }
}

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

