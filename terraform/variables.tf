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

variable "dev_mode" {
  description = "Skip AWS credentials validation"
  type        = bool
  default     = true
}
