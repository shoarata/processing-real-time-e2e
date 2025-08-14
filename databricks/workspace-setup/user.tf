data "databricks_user" "me" {
  user_name = var.db_main_account_email
  provider = databricks.mws
}
resource "databricks_mws_permission_assignment" "add_my_user" {
  provider = databricks.mws
  permissions = ["ADMIN"]
  principal_id = data.databricks_user.me.id
  workspace_id = databricks_mws_workspaces.main_ws.workspace_id
}