# GFT Cloud Data Migration Framework

> **GFT** implements **ThoughtMachine Vault** for **APAC banks** replacing legacy cores (**T24**, **Finacle**, **FLEXCUBE**). This repo includes the **portfolio Python toolkit** (`extractor`, `validator`) and the **`data-migration-infra-main`** snapshot: production-style **AWS Step Functions**, **Glue**, **Iceberg**, **Athena**, **Lambda**, and **EKS** producers used on a live migration program.

**Portfolio reconstruction** — no GFT, ThoughtMachine, or bank customer data. UAT resource names in Glue scripts are placeholders.

## What’s in this repo

| Area | Location | Role |
|------|----------|------|
| **Infra (Terraform)** | `data-migration-infra-main/infra/` | VPC, S3 raw/staging, Glue jobs, Step Functions, Lambda recon |
| **Glue / Lambda ETL** | `data-migration-infra-main/infra/data-etl/python/` | Extract, raw→staging, staging→migration+DQ |
| **TM load (K8s)** | `data-migration-infra-main/backend/dataLoader/` | Kafka producers after migration DB validated |
| **Python toolkit** | `extractor.py`, `validator.py`, `connector_base.py` | Legacy→S3 extract & validation patterns |
| **Pipeline map** | [docs/gft_migration_pipeline.md](docs/gft_migration_pipeline.md) | Script names ↔ migration phases |

## End-to-end flow (GFT delivery)

| Phase | What happens | Outcome |
|-------|----------------|--------|
| **1. Extract** | **PostgreSQL** (migration staging DB) → Glue `glue-job-postgres-to-s3-args.py` → **S3 raw** Parquet | Authoritative snapshots per table |
| **2. Raw → staging** | Glue `sa-*`, `ca-*`, `customer-*`, `loan-*` raw-to-staging jobs → **Glue Catalog** `ext_staging.*` | Conformed account, posting, customer, deposit, loan |
| **3. Staging → migration + DQ** | `*-job-staging-migrationdb.py` + Glue DQ; fails → `dq_fails`; pass → **Iceberg** `ext_migration.*` | TM-ready migration tables |
| **4. Reconciliation** | Lambda + **Athena** compare raw / staging / migration; `sf_global_reconciliation` | Sign-off metrics in log tables |
| **5. ThoughtMachine load** | TM ID matchers + **EKS** Kafka producers → **ThoughtMachine Vault** | Migration complete |

Legacy cores land in PostgreSQL (or S3) first; **ThoughtMachine** is the target after the migration DB passes DQ and recon — then AWS analytics (Redshift / QuickSight) can run in parallel.

## Architecture diagrams

### 1 · Program overview

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '18px'}}}%%
flowchart LR
    ORCH["🎯 Migration<br/>Orchestrator"]
    SF["⚙️ AWS Step Functions<br/>sf_global_migration"]
    TM["🏦 ThoughtMachine<br/>Vault CBS"]

    ORCH -->|"StartExecution"| SF
    SF -->|"Load confirmed"| TM
    SF -->|"Metrics & recon"| ORCH

    style ORCH fill:#FFF9C4,stroke:#F9A825,stroke-width:3px
    style SF fill:#E1BEE7,stroke:#7B1FA2,stroke-width:3px
    style TM fill:#C8E6C9,stroke:#2E7D32,stroke-width:3px
```

### 2 · Phase 1–2 — Extract & raw → staging

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '17px'}}}%%
flowchart TD
    subgraph SRC["📥 Source"]
        PG["PostgreSQL<br/>migration staging DB"]
    end

    subgraph ORCH["🎛️ Orchestration"]
        SF1["Step Functions<br/>per-entity pipelines"]
        GL0["Glue<br/>glue-job-postgres-to-s3-args.py"]
    end

    subgraph RAW["🪣 S3 raw zone"]
        S3R["Parquet<br/>partitioned extracts"]
    end

    subgraph STG["📋 Glue Catalog — staging"]
        direction LR
        ACC["ext_staging.account"]
        CUS["ext_staging.customer"]
        PIB["ext_staging.posting"]
    end

    subgraph JOBS["Glue raw → staging"]
        direction LR
        SA["sa-account-job-raw-to-staging"]
        SP["sa-posting-job-raw-to-staging"]
        CU["customer-raw-to-staging"]
    end

    PG --> GL0
    SF1 --> GL0
    GL0 --> S3R
    S3R --> SA & SP & CU
    SA --> ACC
    SP --> PIB
    CU --> CUS

    style SRC fill:#FFE0B2,stroke:#E65100,stroke-width:2px
    style RAW fill:#BBDEFB,stroke:#1565C0,stroke-width:3px
    style STG fill:#C5CAE9,stroke:#303F9F,stroke-width:3px
    style ORCH fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px
```

### 3 · Phase 3 — Staging → migration + data quality

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '17px'}}}%%
flowchart TD
    subgraph IN["📋 Staging tables"]
        STG["ext_staging.*"]
    end

    subgraph GLUE["⚗️ Glue + DQ"]
        MIG["*-job-staging-migrationdb.py"]
        DQ["EvaluateDataQuality<br/>completeness • uniqueness"]
        DQO["*-job-dq-only.py"]
    end

    subgraph OUT["💾 Outputs"]
        ICE["Iceberg ext_migration.*<br/>S3-backed migration DB"]
        FAIL["dq_fails table"]
    end

  subgraph SF["Step Functions"]
    SFDQ["sf_all_entities_dq_only"]
  end

    STG --> MIG
    STG --> DQO
    MIG --> DQ
    DQ -->|"pass"| ICE
    DQ -->|"fail"| FAIL
    SFDQ -.-> MIG

    style IN fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style GLUE fill:#FFF9C4,stroke:#F9A825,stroke-width:2px
    style OUT fill:#C8E6C9,stroke:#388E3C,stroke-width:3px
    style SF fill:#E1BEE7,stroke:#7B1FA2,stroke-width:2px
```

### 4 · Phase 4–5 — Reconciliation & ThoughtMachine load

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '17px'}}}%%
flowchart TD
    subgraph RECON["✅ Reconciliation"]
        direction LR
        L1["Lambda<br/>raw ↔ staging"]
        L2["Lambda<br/>staging ↔ migration"]
        ATH["Amazon Athena<br/>SQL counts & IDs"]
        LOG["Metrics log table"]
    end

    subgraph MATCH["🔗 TM matching"]
        JM["Glue TM ID matchers<br/>account • posting"]
    end

    subgraph LOAD["🚀 Load"]
        EKS["EKS dataLoader<br/>Kafka producers"]
        TM["ThoughtMachine Vault"]
    end

    ICE["Iceberg migration DB"] --> L2
    STG2["Staging tables"] --> L1
    L1 & L2 --> ATH --> LOG
    ICE --> JM --> EKS --> TM

    style RECON fill:#F8BBD0,stroke:#C2185B,stroke-width:3px
    style MATCH fill:#B2DFDB,stroke:#00695C,stroke-width:2px
    style LOAD fill:#DCEDC8,stroke:#558B2F,stroke-width:3px
```

### 5 · Sequence view (matches PlantUML)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '16px'}}}%%
sequenceDiagram
    autonumber
    participant O as Migration Orchestrator
    participant SF as Step Functions
    participant PG as PostgreSQL
    participant G as AWS Glue
    participant S3 as S3 Raw
    participant ST as Glue Staging
    participant ICE as Iceberg Migration
    participant L as Lambda
    participant A as Athena
    participant TM as ThoughtMachine

    O->>SF: Start migration job
    SF->>G: glue-job-postgres-to-s3-args.py
    G->>PG: JDBC extract
    PG-->>G: chunks
    G->>S3: Parquet files

    SF->>G: sa-account / sa-posting raw-to-staging
    G->>S3: read
    G->>ST: ext_staging.*

    SF->>G: *-staging-migrationdb + DQ
    G->>ST: read
    G->>ICE: pass rows
    G->>ST: dq_fails

    SF->>L: reconciliation Lambdas
    L->>A: query counts / IDs
    A-->>L: results
    L->>A: log metrics

    SF->>TM: load from migration DB
    TM-->>SF: OK
    SF-->>O: Migration complete
```

## Legacy cores → AWS (bank context)

| Core | Typical role in program |
|------|-------------------------|
| **Temenos T24** | COB tables, AA contracts, GL |
| **Finacle** | CIF, accounts, transactions |
| **FLEXCUBE** | Customer, account, collateral |

Extracts are normalized into the **migration PostgreSQL / S3 raw** layout before TM mapping — see [docs/migration_phases.md](docs/migration_phases.md).

## AWS stack

| Service | Role in `data-migration-infra-main` |
|---------|-------------------------------------|
| **Step Functions** | `sf_global_migration`, per-entity `*_raw_to_migration`, DQ, recon |
| **Glue** | JDBC extract, Spark transforms, Glue DQ, Iceberg writes |
| **S3** | Raw + staging warehouse paths |
| **Glue Catalog** | `ext_staging`, `ext_migration`, `dq_fails` |
| **Iceberg** | Migration DB tables on S3 |
| **Lambda + Athena** | Reconciliation & metrics |
| **EKS** | dataLoader producers to ThoughtMachine |
| **Terraform** | `infra/data-etl`, `networking`, `eks` |

## Project layout

```
gft-cloud-data-migration-framework/
├── data-migration-infra-main/     # Terraform + Glue + SF + backend (GFT program)
│   ├── infra/data-etl/python/    # Glue & Lambda scripts
│   └── backend/dataLoader/        # TM Kafka producers
├── connector_base.py
├── extractor.py
├── validator.py
└── docs/
    ├── migration_phases.md        # Legacy → TM → AWS phases
    └── gft_migration_pipeline.md  # Script ↔ layer map
```

## Quick start

```bash
git clone https://github.com/willtran112358/gft-cloud-data-migration-framework.git
cd gft-cloud-data-migration-framework
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

Explore infra: `cd data-migration-infra-main/infra/data-etl && type README.md`

---

**Will Tran** — [@willtran112358](https://github.com/willtran112358)
