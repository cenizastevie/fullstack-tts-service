variable "environment" {
  description = "The environment for the resources"
  type        = string
}

variable "bucket_name_prefix" {
  description = "The prefix for the S3 bucket name"
  type        = string
}

variable "region" {
  description = "The AWS region to deploy to"
  type        = string
}

variable "s3_endpoint" {
  description = "S3 endpoint for LocalStack"
  type        = string
  default     = ""
}

variable "access_key" {
  description = "AWS access key"
  type        = string
  default     = ""
}

variable "secret_key" {
  description = "AWS secret key"
  type        = string
  default     = ""
}

variable "skip_credentials_validation" {
  description = "Skip AWS credentials validation"
  type        = bool
  default     = false
}

variable "skip_metadata_api_check" {
  description = "Skip AWS metadata API check"
  type        = bool
  default     = false
}

variable "skip_requesting_account_id" {
  description = "Skip requesting AWS account ID"
  type        = bool
  default     = false
}

variable "s3_use_path_style" {
  description = "Use path-style URLs for S3"
  type        = bool
  default     = false
}
