variable "environment" {
  description = "The environment for the resources"
  type        = string
  default     = "dev"
}

variable "bucket_name_prefix" {
  description = "The prefix for the S3 bucket name"
  type        = string
  default     = "myproject"
}

variable "s3_endpoint" {
  description = "S3 endpoint for LocalStack"
  type        = string
  default     = "http://localhost:4566"
}

variable "skip_credentials_validation" {
  description = "Skip AWS credentials validation"
  type        = bool
  default     = true
}

variable "skip_metadata_api_check" {
  description = "Skip metadata API check"
  type        = bool
  default     = true
}

variable "skip_requesting_account_id" {
  description = "Skip id check"
  type        = bool
  default     = true
}
