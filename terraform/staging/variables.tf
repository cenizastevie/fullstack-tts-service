variable "environment" {
  description = "The environment for the resources"
  type        = string
  default     = "staging"
}

variable "bucket_name_prefix" {
  description = "The prefix for the S3 bucket name"
  type        = string
  default     = "tts-service"
}

variable "region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}


variable "mysqlpassword" {
  description = "The password for the MySQL database"
  type        = string
  default     = "password"
}