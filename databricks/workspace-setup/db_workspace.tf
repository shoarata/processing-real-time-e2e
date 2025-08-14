resource "databricks_mws_workspaces" "main_ws" {
  provider = databricks.mws
  account_id     = var.db_account_id
  workspace_name = "${var.resource_prefix}_workspace"
  aws_region = var.aws_region
  credentials_id = databricks_mws_credentials.this.credentials_id
  storage_configuration_id = databricks_mws_storage_configurations.this.storage_configuration_id
  network_id = databricks_mws_networks.this.network_id
}

output "databricks_host" {
  value = databricks_mws_workspaces.main_ws.workspace_url
}