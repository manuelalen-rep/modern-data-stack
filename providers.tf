terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "1.25.0"
    }
  }
}

provider "postgresql" {
  host            = "localhost"
  port            = 5432
  database        = "postgres" # Entramos por la puerta de servicio para crear las demás
  username        = "admin"
  password        = "password123"
  sslmode         = "disable"
}