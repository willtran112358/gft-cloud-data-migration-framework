resource "aws_glue_catalog_database" "tm_migration_database-migration" {
  name = "${var.environment}_migrationdb"
}

resource "aws_glue_catalog_database" "tm_migration_database-staging" {
  name = "${var.environment}_staging"
}

resource "aws_glue_catalog_database" "tm_migration_database-raw" {
  name = "${var.environment}_rawdb"
}
