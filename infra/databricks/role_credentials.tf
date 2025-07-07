data "databricks_aws_assume_role_policy" "this" {
  external_id = var.db_account_id
  provider = databricks.mws
}
resource "aws_iam_role" "databricks_cross_account_role" {
  name = "${var.resource_prefix}cross_account_role"
  assume_role_policy = data.databricks_aws_assume_role_policy.this.json
}
data "databricks_aws_crossaccount_policy" "this" {
  provider = databricks.mws
  policy_type = "customer"
}
resource "aws_iam_role_policy" "this" {
  policy = data.databricks_aws_crossaccount_policy.this.json
  role   = aws_iam_role.databricks_cross_account_role.id
}
resource "databricks_mws_credentials" "this" {
  credentials_name = "${var.resource_prefix}credentials"
  role_arn         = aws_iam_role.databricks_cross_account_role.arn
  provider = databricks.mws
  depends_on = [aws_iam_role_policy.this]
}