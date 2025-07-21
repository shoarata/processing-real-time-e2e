terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    bucket = "terraform-backend-sho"
    key = "ecommenrce-project/databricks"
    use_lockfile = true
  }
}
provider "databricks" {
  alias = "mws"
  host = "https://accounts.cloud.databricks.com"
  account_id = var.db_account_id
  client_id = var.db_client_id
  client_secret = var.db_client_secret
}
provider "aws" {
  region = var.aws_region
}