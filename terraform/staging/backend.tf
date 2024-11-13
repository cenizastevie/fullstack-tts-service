terraform {
  backend "s3" {
    bucket                  = "tts-service-staging-terraform-state"
    key                     = "terraform.tfstate"
    region                  = "us-east-1"
  }
}