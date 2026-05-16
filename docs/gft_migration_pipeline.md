# GFT data migration pipeline — script & layer map

Maps the **PlantUML sequence** (Migration Orchestrator → Step Functions → Glue → Iceberg → Lambda/Athena → ThoughtMachine) to code under `data-migration-infra-main/`.

> Portfolio snapshot — UAT bucket/account names appear in Glue scripts; treat as non-production placeholders.

## Data layers

| Layer | Glue Catalog / Iceberg | Purpose |
|-------|------------------------|---------|
| **Raw** | S3 `…-raw` Parquet drops | JDBC extract from PostgreSQL (legacy-shaped staging DB) |
| **Staging** | `uat_staging` / `ext_staging.*` | Conformed entities: account, customer, posting, deposit, loan |
| **Migration** | `ext_migration.*` (Iceberg on S3) | DQ-gated tables ready for TM load |
| **DQ fails** | `dq_fails` | Rows failing Glue Data Quality rules |

## Phase 1 — Data extraction

| Step | Component | Script / resource |
|------|-----------|-------------------|
| Orchestrator starts job | `aws_sfn_state_machine.sf_global_migration` | `infra/data-etl/stepfunctions/sf_global_migration.asl.json` |
| Postgres → S3 Parquet | Glue `glue-job-postgres-to-s3-args.py` | JDBC chunks → `s3://…-raw` |

## Phase 2 — Raw → staging

| Entity | Glue job (examples) |
|--------|---------------------|
| Savings account | `sa-account-job-raw-to-staging.py` |
| Savings posting | `sa-posting-job-raw-to-staging.py` |
| Current account | `ca-account-job-raw-to-staging.py`, `ca-posting-job-raw-to-staging.py` |
| Customer | `customer-raw-to-staging.py` |
| Loan | `loan-account-job-raw-to-staging.py`, `loan-posting-job-raw-to-staging.py` |
| Overdraft | `od-account-job-raw-to-staging.py`, `od-posting-job-raw-to-staging.py` |

Per-entity Step Functions: `sf_customer_raw_to_migration`, `sf_account_raw_to_migration`, `sf_posting_raw_to_migration`, `sf_deposit_raw_to_migration`, `sf_loan_raw_to_migration`.

## Phase 3 — Staging → migration + DQ

| Entity | Staging → migration (DQ) | DQ-only |
|--------|--------------------------|---------|
| Account | `account-job-staging-migrationdb.py` | `account-job-dq-only.py` |
| Customer | `customer-job-staging-migrationdb.py` | `customer-job-dq-only.py` |
| Posting | `posting-job-staging-migrationdb.py` | `posting-job-dq-only.py` |
| Deposit | `deposit-job-staging-migrationdb.py` | `deposit-job-dq-only.py` |
| Loan | `loan-job-staging-migrationdb.py` | `loan-job-dq-only.py` |

Uses **AWS Glue Data Quality** (`EvaluateDataQuality`) — pass rows → Iceberg migration DB; fails → `dq_fails`.

Orchestrated by `sf_all_entities_dq_only` and entity `*_raw_to_migration` state machines.

## Phase 4 — Reconciliation

| Check | Lambda (Athena queries) |
|-------|-------------------------|
| Raw vs staging files | `lambda-reconciliation-files-raw.py` |
| Raw vs staging (generic) | `lambda-reconciliation-raw-staging.py` |
| Staging vs migration | `lambda-reconciliation-staging-migration.py` |
| Deposit staging vs migration | `lambda-reconciliation-deposit-staging-migration.py` |
| Loan staging vs migration | `lambda-reconciliation-loan-staging-migration.py` |
| Posting staging vs migration | `lambda-reconciliation-posting-staging-migration.py` |
| Global / EKS reconciliator | `sf_global_reconciliation` + `backend/global-reconciliator*` |

Metrics / counts: `lambda-count-unreconcilied-entities.py`, `lambda-history.py`.

## Phase 5 — ThoughtMachine load

| Step | Component |
|------|-----------|
| TM ID matching | `job-account-tm-id-matcher.py`, `job-posting-tm-id-matcher.py` |
| Kafka producers (K8s) | `backend/dataLoader/src/*_producer.py` |
| Deploy producers | `sf_deploy_job_producer_customer`, `_account`, `_posting` |

## Infra layout (`data-migration-infra-main/`)

```
data-migration-infra-main/
├── infra/
│   ├── data-etl/          # Glue, Lambda, Step Functions, IAM
│   │   ├── python/        # 35 Glue/Lambda scripts
│   │   └── stepfunctions/ # ASL definitions
│   ├── networking/        # VPC, S3, KMS
│   ├── eks/               # TM dataLoader on Kubernetes
│   └── base-deployment/   # ECR, shared KMS
├── backend/
│   ├── dataLoader/        # Kafka producers → ThoughtMachine
│   └── global-reconciliator*/
└── config/
    ├── framework_config.json
    └── environment_config.json
```

Terraform entry point for ETL: `infra/data-etl/` (see `README.md` in that module).
