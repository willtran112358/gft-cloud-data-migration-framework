
resource "aws_s3_object" "customer-job-staging-migrationdb" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/customer-job-staging-migrationdb.py" # Cambia esto al nombre de tu archivo
  source = "python/customer-job-staging-migrationdb.py"   # Ruta local de tu archivo

}

resource "aws_s3_object" "account-job-staging-migrationdb" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/account-job-staging-migrationdb.py" # Cambia esto al nombre de tu archivo
  source = "python/account-job-staging-migrationdb.py"   # Ruta local de tu archivo

}

resource "aws_s3_object" "posting-job-staging-migrationdb" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/posting-job-staging-migrationdb.py" # Cambia esto al nombre de tu archivo
  source = "python/posting-job-staging-migrationdb.py"   # Ruta local de tu archivo

}

resource "aws_s3_object" "deposit-job-staging-migrationdb" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/deposit-job-staging-migrationdb.py" # Cambia esto al nombre de tu archivo
  source = "python/deposit-job-staging-migrationdb.py"   # Ruta local de tu archivo

}

resource "aws_s3_object" "loan-job-staging-migrationdb" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/loan-job-staging-migrationdb.py" # Cambia esto al nombre de tu archivo
  source = "python/loan-job-staging-migrationdb.py"   # Ruta local de tu archivo

}


resource "aws_glue_job" "customer_staging_migrationdb" {
  depends_on  = [aws_s3_object.customer-job-staging-migrationdb]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
    "--execution_id"                     = "1:Manual_Execution"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-customer-staging-migrationdb"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/customer-job-staging-migrationdb.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_glue_job" "account_staging_migrationdb" {
  depends_on  = [aws_s3_object.account-job-staging-migrationdb]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
    "--execution_id"                     = "1:Manual_Execution"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-account-staging-migrationdb"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/account-job-staging-migrationdb.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_glue_job" "posting_staging_migrationdb" {
  depends_on  = [aws_s3_object.posting-job-staging-migrationdb]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
    "--execution_id"                     = "1:Manual_Execution"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-posting-staging-migrationdb"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/posting-job-staging-migrationdb.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

# empty job for posting calculator
resource "aws_s3_object" "posting_balance_calculator" {
  count  = var.create_balance_calculator_job ? 1 : 0
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/posting_balance_calculator.py" # Cambia esto al nombre de tu archivo
  source = "python/posting_balance_calculator.py"   # Ruta local de tu archivo

}

resource "aws_glue_job" "posting_balance_calculator" {
  depends_on  = [aws_s3_object.posting_balance_calculator]
  count       = var.create_balance_calculator_job ? 1 : 0
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=file:///tmp/spark-warehouse --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
    "--execution_id"                     = "1:Manual_Execution"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-posting-balance-calculator"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/posting_balance_calculator.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_glue_job" "deposit_staging_migrationdb" {
  depends_on  = [aws_s3_object.deposit-job-staging-migrationdb]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=file:///tmp/spark-warehouse --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
    "--execution_id"                     = "1:Manual_Execution"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-deposit-staging-migrationdb"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/deposit-job-staging-migrationdb.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_glue_job" "loan_staging_migrationdb" {
  depends_on  = [aws_s3_object.loan-job-staging-migrationdb]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
    "--execution_id"                     = "1:Manual_Execution"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-loan-staging-migrationdb"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/loan-job-staging-migrationdb.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

########### Matcher Jobs ###########
# Account Matcher

resource "aws_s3_object" "account_tm_id_matcher" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/job-account-tm-id-matcher.py" # Cambia esto al nombre de tu archivo
  source = "python/job-account-tm-id-matcher.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "account_tm_id_matcher" {
  depends_on  = [aws_s3_object.account_tm_id_matcher]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-account-tm-id-matcher"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/job-account-tm-id-matcher.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

# Posting Matcher

resource "aws_s3_object" "posting_tm_id_matcher" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/job-posting-tm-id-matcher.py" # Cambia esto al nombre de tu archivo
  source = "python/job-posting-tm-id-matcher.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "posting_tm_id_matcher" {
  depends_on  = [aws_s3_object.posting_tm_id_matcher]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-posting-tm-id-matcher"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/job-posting-tm-id-matcher.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

##################################
###  DQ Only Jobs             ####
##################################
#Customer 
resource "aws_s3_object" "customer_dq_only" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/customer-job-dq-only.py" # Cambia esto al nombre de tu archivo
  source = "python/customer-job-dq-only.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "customer_dq_only" {
  depends_on  = [aws_s3_object.posting_tm_id_matcher]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-customer-job-dq-only"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/customer-job-dq-only.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

#Account 
resource "aws_s3_object" "account_dq_only" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/account-job-dq-only.py" # Cambia esto al nombre de tu archivo
  source = "python/account-job-dq-only.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "account_dq_only" {
  depends_on  = [aws_s3_object.account_dq_only]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-account-job-dq-only"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/account-job-dq-only.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

#Posting 
resource "aws_s3_object" "posting_dq_only" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/posting-job-dq-only.py" # Cambia esto al nombre de tu archivo
  source = "python/posting-job-dq-only.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "posting_dq_only" {
  depends_on  = [aws_s3_object.posting_dq_only]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-posting-job-dq-only"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/posting-job-dq-only.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

#deposit 
resource "aws_s3_object" "deposit_dq_only" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/deposit-job-dq-only.py" # Cambia esto al nombre de tu archivo
  source = "python/deposit-job-dq-only.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "deposit_dq_only" {
  depends_on  = [aws_s3_object.posting_tm_id_matcher]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-deposit-job-dq-only"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/deposit-job-dq-only.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

#loan 
resource "aws_s3_object" "loan_dq_only" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/loan-job-dq-only.py" # Cambia esto al nombre de tu archivo
  source = "python/loan-job-dq-only.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "loan_dq_only" {
  depends_on  = [aws_s3_object.posting_tm_id_matcher]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }
  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-loan-job-dq-only"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/loan-job-dq-only.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_s3_object" "postgres_to_s3" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/glue-job-postgres-to-s3.py"
  source = "python/glue-job-postgres-to-s3.py"
}

resource "aws_glue_job" "postgres_to_s3" {
  depends_on  = [aws_s3_object.postgres_to_s3]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--table_name"                       = "customer"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-language"                     = "python"
    "--execution_id"                     = "1:Manual_Execution"
    "--enable-glue-datacatalog"          = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-postgres-to-s3"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/glue-job-postgres-to-s3.py"
  }

  execution_property {
    max_concurrent_runs = 4
  }
}

resource "aws_s3_object" "raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/glue-job-raw-to-staging.py"
  source = "python/glue-job-raw-to-staging.py"
}

resource "aws_glue_job" "raw_to_staging" {
  depends_on  = [aws_s3_object.raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--table_name"                       = "customer"
    "--job-language"                     = "python"
    "--enable-glue-datacatalog"          = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/glue-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}
# OD Migration
resource "aws_s3_object" "script_postgres_to_s3_args" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/glue-job-postgres-to-s3-args.py" # Cambia esto al nombre de tu archivo
  source = "python/glue-job-postgres-to-s3-args.py"   # Ruta local de tu archivo
}

resource "aws_glue_job" "generic_postgres_to_s3" {
  depends_on  = [aws_s3_object.script_postgres_to_s3_args]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--job-language"                     = "python"
    "--enable-glue-datacatalog"          = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "${var.prefix}-postgres-to-s3-generic"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/glue-job-postgres-to-s3-args.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}



resource "aws_s3_object" "sa_account_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/sa-account-job-raw-to-staging.py"
  source = "python/sa-account-job-raw-to-staging.py"
}

resource "aws_glue_job" "sa_account_job_raw_to_staging" {
  depends_on  = [aws_s3_object.sa_account_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--table_name"                       = "customer"
    "--job-language"                     = "python"
    "--execution_id"                     = "1:Manual_Execution"
    "--enable-glue-datacatalog"          = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "sa-account-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_s3_object" "sa_posting_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/sa-posting-job-raw-to-staging.py"
  source = "python/sa-posting-job-raw-to-staging.py"
}

resource "aws_glue_job" "sa_posting_job_raw_to_staging" {
  depends_on  = [aws_s3_object.sa_posting_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--table_name"                       = "sa_posting"
    "--job-language"                     = "python"
    "--enable-glue-datacatalog"          = "true"
    "--execution_id"                     = "1:Manual_Execution"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "sa-posting-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_s3_object" "ca_account_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/ca-account-job-raw-to-staging.py"
  source = "python/ca-account-job-raw-to-staging.py"
}

resource "aws_glue_job" "ca_account_job_raw_to_staging" {
  depends_on  = [aws_s3_object.ca_account_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--table_name"                       = "ca_account"
    "--job-language"                     = "python"
    "--execution_id"                     = "1:Manual_Execution"
    "--enable-glue-datacatalog"          = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "ca-account-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_s3_object" "ca_posting_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/ca-posting-job-raw-to-staging.py"
  source = "python/ca-posting-job-raw-to-staging.py"
}

resource "aws_glue_job" "ca_posting_job_raw_to_staging" {
  depends_on  = [aws_s3_object.ca_posting_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--table_name"                       = "ca_posting"
    "--job-language"                     = "python"
    "--enable-glue-datacatalog"          = "true"
    "--execution_id"                     = "1:Manual_Execution"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "ca-posting-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_s3_object" "od_account_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/od-account-job-raw-to-staging.py"
  source = "python/od-account-job-raw-to-staging.py"
}

resource "aws_glue_job" "od_account_job_raw_to_staging" {
  depends_on  = [aws_s3_object.od_account_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--table_name"                       = "od_account"
    "--job-language"                     = "python"
    "--enable-glue-datacatalog"          = "true"
    "--execution_id"                     = "1:Manual_Execution"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "od-account-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_s3_object" "od_posting_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/od-posting-job-raw-to-staging.py"
  source = "python/od-posting-job-raw-to-staging.py"
}

resource "aws_glue_job" "od_posting_job_raw_to_staging" {
  depends_on  = [aws_s3_object.od_posting_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--table_name"                       = "od_posting"
    "--job-language"                     = "python"
    "--enable-glue-datacatalog"          = "true"
    "--execution_id"                     = "1:Manual_Execution"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "od-posting-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_s3_object" "loan_account_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/loan-account-job-raw-to-staging.py"
  source = "python/loan-account-job-raw-to-staging.py"
}

resource "aws_glue_job" "loan_account_job_raw_to_staging" {
  depends_on  = [aws_s3_object.loan_account_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--table_name"                       = "loan_account"
    "--job-language"                     = "python"
    "--execution_id"                     = "1:Manual_Execution"
    "--enable-glue-datacatalog"          = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "loan-account-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}


resource "aws_s3_object" "loan_posting_job_raw_to_staging" {
  bucket = "aws-glue-assets-${local.account_id}-${var.region}"
  key    = "/scripts/loan-posting-job-raw-to-staging.py"
  source = "python/loan-posting-job-raw-to-staging.py"
}

resource "aws_glue_job" "loan_posting_job_raw_to_staging" {
  depends_on  = [aws_s3_object.loan_posting_job_raw_to_staging]
  connections = []
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-${local.account_id}-${var.region}/temporary/"
    "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.warehouse=s3://699955796816-ap-southeast-1-gft-dm-uat-staging/tables --conf spark.sql.iceberg.handle-timestamp-without-timezone=true"
    "--datalake-formats"                 = "iceberg"
    "--table_name"                       = "loan_posting"
    "--job-language"                     = "python"
    "--enable-glue-datacatalog"          = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-job-insights"              = "false"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
    "--execution_id"                     = "1:Manual_Execution"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-${local.account_id}-${var.region}/sparkHistoryLogs/"
  }

  execution_class           = "STANDARD"
  glue_version              = "4.0"
  max_retries               = 0
  name                      = "loan-posting-job-raw-to-staging"
  non_overridable_arguments = {}
  number_of_workers         = var.number_of_workers
  role_arn                  = "arn:aws:iam::${local.account_id}:role/${var.prefix}-AWSGlueServiceRole"
  timeout                   = 2880
  worker_type               = var.worker_type

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://aws-glue-assets-${local.account_id}-${var.region}/scripts/sa-account-job-raw-to-staging.py"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}