resource "aws_glue_crawler" "glue_crawler" {
  for_each    = var.s3_source_files_dirs
  classifiers = []
  configuration = jsonencode(
    {
      CreatePartitionIndex = true
      Version              = 1
    }
  )
  database_name = aws_glue_catalog_database.tm_migration_database-raw.name
  name          = "crawler-${each.key}"
  # role          = "AWSGlueServiceRole"
  # HDBank edit
  role          = "${var.prefix}-AWSGlueServiceRole"
  tags          = var.csv-raw-crawler-tags
  tags_all      = {}
  lake_formation_configuration {
    use_lake_formation_credentials = false
  }
  lineage_configuration {
    crawler_lineage_settings = "DISABLE"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_EVERYTHING"
  }
  s3_target {
    exclusions = []
    path       = "s3://${module.s3_source_files.bucket_id}/${each.key}/"
  }

  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
    update_behavior = "UPDATE_IN_DATABASE"
  }
}

resource "aws_glue_crawler" "glue_crawler_global_reconciliation" {
  for_each    = var.s3_source_files_dirs
  classifiers = []
  configuration = jsonencode(
    {
      CreatePartitionIndex = true
      Version              = 1
    }
  )
  database_name = aws_glue_catalog_database.tm_migration_database-migration.name
  name          = "crawler-global-reconciliation-${each.key}"
  # role          = "AWSGlueServiceRole"
  # HDBank edit
  role          = "${var.prefix}-AWSGlueServiceRole"
  table_prefix  = "global_reconciliator_"
  tags          = var.global-reconciliation-crawler-tags
  tags_all      = {}
  lake_formation_configuration {
    use_lake_formation_credentials = false
  }
  lineage_configuration {
    crawler_lineage_settings = "DISABLE"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_EVERYTHING"
  }
  s3_target {
    exclusions = []
    path       = "s3://${module.s3_migration.bucket_id}/reconciliator-files/final_parquet/${each.key}/"
  }

  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
    update_behavior = "UPDATE_IN_DATABASE"
  }
}