module "shared" {
  source = "../shared"

  environment                   = "staging"
  bucket_name_prefix            = "tts-service"
  region                        = "us-east-1"
  access_key                    = var.access_key
  secret_key                    = var.secret_key
}