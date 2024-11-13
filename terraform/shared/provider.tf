provider "aws" {
  region                      = var.region
  access_key                  = var.access_key
  secret_key                  = var.secret_key
  skip_credentials_validation = var.skip_credentials_validation
  skip_metadata_api_check     = var.skip_metadata_api_check
  skip_requesting_account_id  = var.skip_requesting_account_id
  s3_use_path_style           = var.s3_use_path_style

  endpoints {
    s3             = var.s3_endpoint
    ec2            = var.s3_endpoint
    ecs            = var.s3_endpoint
    iam            = var.s3_endpoint
    apigatewayv2   = var.s3_endpoint
  }
}