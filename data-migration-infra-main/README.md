# GFT data migration infrastructure (portfolio)

Terraform + AWS Glue + Step Functions + Lambda + EKS workloads for **ThoughtMachine Vault** migration programs.

**Documentation:** see the parent repo [README](../README.md) and [docs/gft_migration_pipeline.md](../docs/gft_migration_pipeline.md).

| Module | Path |
|--------|------|
| ETL & orchestration | `infra/data-etl/` |
| Networking & raw S3 | `infra/networking/` |
| EKS (dataLoader producers) | `infra/eks/` |
| Backend services | `backend/dataLoader/`, `backend/global-reconciliator*/` |

> Snapshot for portfolio review — scrub account IDs and secrets before any non-demo deploy.
