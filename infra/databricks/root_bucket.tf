resource "aws_s3_bucket" "root_storage_bucket" {
  bucket = replace("${var.resource_prefix}root_bucket", "_", "-")
  force_destroy = true
}
resource "aws_s3_bucket_server_side_encryption_configuration" "root_storage_bucket_ssec" {
  bucket = aws_s3_bucket.root_storage_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "root_storage_bucket" {
  bucket = aws_s3_bucket.root_storage_bucket.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
  depends_on = [aws_s3_bucket.root_storage_bucket]
}

data "databricks_aws_bucket_policy" "this" {
  bucket = aws_s3_bucket.root_storage_bucket.bucket
}

resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.root_storage_bucket.id
  policy = data.databricks_aws_bucket_policy.this.json
  depends_on = [aws_s3_bucket_public_access_block.root_storage_bucket]
}

resource "aws_s3_bucket_versioning" "root_bucket_versioning" {
  bucket = aws_s3_bucket.root_storage_bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}

resource "databricks_mws_storage_configurations" "this" {
  provider = databricks.mws
  account_id                 = var.db_account_id
  bucket_name                = aws_s3_bucket.root_storage_bucket.bucket
  storage_configuration_name = "${var.resource_prefix}_storage"
}