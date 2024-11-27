module "shared" {
  source = "../shared"

  environment                   = var.environment 
  bucket_name_prefix            = var.bucket_name_prefix 
  region                        = var.region 
}