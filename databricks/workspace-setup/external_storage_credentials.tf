
data "databricks_aws_unity_catalog_policy" "this" {
  aws_account_id = var.aws_account_id
  bucket_name    = var.aws_external_data_s3_bucket_name
  role_name      = "${var.resource_prefix}uc_access"
}

data "databricks_aws_unity_catalog_assume_role_policy" "this" {
  aws_account_id = var.aws_account_id
  role_name      = "${var.resource_prefix}uc_access"
  external_id    = var.db_account_id
}

resource "aws_iam_policy" "unity_metastore" {
  name   = "${var.resource_prefix}-unity-catalog-metastore-access-iam-policy"
  policy = data.databricks_aws_unity_catalog_policy.this.json
}

resource "aws_iam_role" "external_storage_access_role" {
  name                = "${var.resource_prefix}uc_access"
  assume_role_policy  = data.databricks_aws_unity_catalog_assume_role_policy.this.json
}

resource "aws_iam_role_policy_attachment" "metastore_data_access" {
  role       = aws_iam_role.external_storage_access_role.name
  policy_arn = aws_iam_policy.unity_metastore.arn
}
resource "databricks_storage_credential" "external" {
  name = "external_storage_s3"
  aws_iam_role {
    role_arn = aws_iam_role.external_storage_access_role.arn
  }
  provider = databricks.ws
  force_destroy = true
}
