module "shared" {
  source = "../shared"

  environment                   = var.environment
  bucket_name_prefix            = var.bucket_name_prefix
  region                        = var.region
  s3_endpoint                   = var.s3_endpoint
  access_key                    = var.access_key
  secret_key                    = var.secret_key
  skip_credentials_validation   = var.skip_credentials_validation
  skip_metadata_api_check       = var.skip_metadata_api_check
  skip_requesting_account_id    = var.skip_requesting_account_id
  s3_use_path_style             = var.s3_use_path_style
}