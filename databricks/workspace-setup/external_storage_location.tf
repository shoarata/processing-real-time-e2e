resource "databricks_external_location" "s3_external_storage" {
  name            = "s3_external"
  url             = "s3://${var.aws_external_data_s3_bucket_name}/db_external"
  credential_name = databricks_storage_credential.external.name
  provider = databricks.ws
}

resource "databricks_grants" "external_location_access_me" {
  external_location = databricks_external_location.s3_external_storage.id
  grant {
    principal = data.databricks_user.me.user_name
    privileges = ["ALL_PRIVILEGES"]
  }
  provider = databricks.ws
}