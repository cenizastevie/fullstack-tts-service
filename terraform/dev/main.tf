module "shared" {
  source                      = "../shared"  # Points to the shared module

  environment                 = "dev"
  bucket_name_prefix          = "tts-service"
  region                      = "us-east-1"
  s3_endpoint                 = "http://localhost:4566"  # LocalStack for development
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = false
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
}
