# --- 1. BASES DE DATOS ---
resource "postgresql_database" "modern_data_stack" {
  name = "modern_data_stack"
}

resource "postgresql_database" "airflow_db" {
  name = "airflow_db"
}

# --- 2. SEGURIDAD ---
resource "postgresql_role" "planner_role" {
  name = "planner"
}

resource "postgresql_role" "planner_user" {
  name     = "planner_user"
  login    = true
  password = "planner"
  roles    = [postgresql_role.planner_role.name]
}

# --- 3. ESQUEMAS ---
resource "postgresql_schema" "layers" {
  for_each = toset(["bronze", "silver", "gold", "analytics"])
  name     = each.value
  database = postgresql_database.modern_data_stack.name
}

# --- 4. PERMISOS ---
resource "postgresql_grant" "db_connect" {
  for_each    = toset([postgresql_role.planner_role.name, postgresql_role.planner_user.name])
  database    = postgresql_database.modern_data_stack.name
  role        = each.value
  object_type = "database"
  privileges  = ["ALL"]
}

resource "postgresql_grant" "schema_access" {
  for_each    = postgresql_schema.layers
  database    = postgresql_database.modern_data_stack.name
  role        = postgresql_role.planner_role.name
  schema      = each.value.name
  object_type = "schema"
  privileges  = ["USAGE", "CREATE"]
}

# --- 5. EL ARCHIVO DE PERFILES (profiles.yml) ---
resource "local_file" "dbt_profile" {
  filename = "${path.module}/dbt_transformation/profiles.yml"
  content  = <<EOT
modern_data_pipeline:
  target: dev
  outputs:
    dev:
      type: postgres
      host: postgres_db
      user: planner_user
      pass: planner
      port: 5432
      dbname: modern_data_stack
      schema: analytics
      threads: 4
EOT
}