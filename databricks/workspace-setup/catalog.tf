resource "databricks_catalog" "main_catalog" {
  name    = "main"
  provider = databricks.ws
  storage_root = databricks_external_location.s3_external_storage.url
}
resource "databricks_grants" "main_grants_me" {
  catalog = databricks_catalog.main_catalog.name
  grant {
    principal = data.databricks_user.me.user_name
    privileges = ["ALL_PRIVILEGES"]
  }
  provider = databricks.ws
}