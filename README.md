# GFT Cloud Data Migration Framework

> **GFT** delivers **ThoughtMachine Vault** programs for **APAC banks** replacing legacy cores. The **reference architecture** below is the industry pattern GFT uses across the region: **legacy extract → S3 landing → TM mapping & load → AWS analytics & cutover**. The folder `data-migration-infra-main/` is one **program implementation** (Glue, Step Functions, Iceberg) — useful as a code sample, not the only valid design for every APAC bank.

**Portfolio reconstruction** — no GFT, ThoughtMachine, or customer data.

## End-to-end flow (APAC standard)

| Phase | What happens | Outcome |
|-------|----------------|--------|
| **1. Legacy extract** | Bank **legacy core** exports GL, contracts, customers, balances to **S3** landing (COB / batch) | Raw legacy zone (`s3://…/legacy/`) |
| **2. TM mapping & load** | **Glue** (or batch) transforms legacy → **ThoughtMachine Vault** schema; GFT mapping packs; bulk/API load | Vault populated — accounts, contracts, postings |
| **3. AWS analytics & cutover** | TM **API/CDC** + legacy S3 → medallion lake → **Redshift**; **MSK** events; **QuickSight** sign-off | Parity reports, reconciliation, legacy decommission |

ThoughtMachine is **not** the first hop from the old core. Legacy lands on **S3** first; only after mapping/load does Vault hold production-shaped CBS data.

## APAC legacy core banking (typical sources)

| Core | Vendor / footprint | Typical extract entities |
|------|-------------------|---------------------------|
| **Temenos T24 / Transact** | Widely used AU, NZ, SEA, India | `CUSTOMER`, AA arrangements, `STMT_ENTRY`, GL, COB snapshots |
| **Finacle** | Infosys — common India, PH, MY, VN partners | CIF, account master, transactions, GL |
| **Oracle FLEXCUBE** | Universal banking, Islamic variants | Customer, account, collateral, GL |
| **Temenos Triple A / Wealth** | Wealth-heavy APAC programs | Portfolio, positions (alongside T24) |
| **Finastra / Misys** | Selected AU & regional installs | Lending, treasury feeds |
| **In-house / vendor CBS** | Smaller regional banks | File-based COB exports → same S3 contract |

Banks usually migrate **one** primary core per program. GFT standardizes extracts into a **common S3 layout** (partition by COB date, source system, entity) before **ThoughtMachine-specific** mapping.

> **Note:** `data-migration-infra-main/` uses a **PostgreSQL staging DB + Iceberg migration layer** pattern from a **single European-program** snapshot. APAC programs (e.g. T24 COB → S3 directly) often **skip** that hop — see [docs/gft_migration_pipeline.md](docs/gft_migration_pipeline.md) for script-level detail only.

## Architecture diagrams

### 1 · Three-phase program (overview)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '18px'}}}%%
flowchart LR
    P1["Phase 1<br/>🏦 Legacy cores<br/>T24 • Finacle • FLEXCUBE"]
    P2["Phase 2<br/>☁️ S3 + Glue<br/>TM mapping & load"]
    P3["Phase 3<br/>📊 AWS lake<br/>Recon & cutover"]

    P1 -->|"COB extracts"| P2
    P2 -->|"Vault go-live data"| P3

    style P1 fill:#FFCDD2,stroke:#C62828,stroke-width:3px,color:#4a0000
    style P2 fill:#FFF9C4,stroke:#F9A825,stroke-width:3px,color:#4a4000
    style P3 fill:#C8E6C9,stroke:#2E7D32,stroke-width:3px,color:#1b3d1b
```

### 2 · Phase 1 — Legacy extract to S3

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '17px'}}}%%
flowchart TD
    subgraph LEGACY["🏦 Legacy cores (on-prem / hosted)"]
        direction LR
        T24["Temenos T24<br/>Transact"]
        FIN["Finacle"]
        FC["FLEXCUBE"]
        OTH["Other CBS<br/>files / DB"]
    end

    subgraph EXTRACT["📥 Extract patterns"]
        direction LR
        COB["COB batch<br/>JDBC / files"]
        API["API / CDC<br/>where available"]
    end

    subgraph LAND["🪣 S3 legacy landing"]
        BRZ["Bronze zone<br/>Parquet • COB partitions"]
        MAN["Manifest<br/>row counts • checksums"]
    end

    T24 & FIN & FC & OTH --> COB & API
    COB & API --> BRZ
    BRZ --> MAN

    style LEGACY fill:#FFEBEE,stroke:#C62828,stroke-width:3px
    style EXTRACT fill:#FFE0B2,stroke:#E65100,stroke-width:2px
    style LAND fill:#BBDEFB,stroke:#1565C0,stroke-width:3px
```

### 3 · Phase 2 — S3 → ThoughtMachine Vault

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '17px'}}}%%
flowchart TD
    subgraph S3["🪣 S3 legacy bronze"]
        RAW["Partitioned extracts<br/>per core / COB date"]
    end

    subgraph ETL["⚙️ Transform & validate"]
        direction LR
        GLUE["AWS Glue / Spark<br/>GFT mapping packs"]
        VAL["validator.py<br/>row • schema • rules"]
        QUAR["Quarantine prefix<br/>failed rows"]
    end

    subgraph TM["🏦 ThoughtMachine Vault"]
        direction LR
        MAP["Customer • Contract<br/>Balance • Posting"]
        LOAD["Bulk ingest / API"]
    end

    RAW --> GLUE
    GLUE --> VAL
    VAL -->|"pass"| MAP
    VAL -->|"fail"| QUAR
    MAP --> LOAD

    style S3 fill:#BBDEFB,stroke:#1565C0,stroke-width:2px
    style ETL fill:#FFF9C4,stroke:#F9A825,stroke-width:2px
    style TM fill:#C8E6C9,stroke:#388E3C,stroke-width:3px
```

### 4 · Phase 3 — AWS data platform & cutover

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '17px'}}}%%
flowchart TD
    subgraph SOURCES["📡 Ongoing feeds"]
        direction LR
        TMAPI["ThoughtMachine<br/>API / CDC"]
        LEG["S3 legacy<br/>parity snapshots"]
    end

    subgraph LAKE["🏅 Medallion lake"]
        direction LR
        SIL["Silver<br/>conformed"]
        GLD["Gold<br/>GL • regulatory"]
    end

    subgraph AWS["☁️ AWS services"]
        direction LR
        MSK["Amazon MSK<br/>events"]
        GL["Glue ETL"]
        RS["Redshift<br/>migration DWH"]
    end

    subgraph OUT["📊 Consumption & controls"]
        direction LR
        RECON["Reconciliation<br/>Legacy ↔ TM ↔ DWH"]
        QS["QuickSight<br/>cutover dashboards"]
    end

    TMAPI --> MSK
    TMAPI --> SIL
    LEG --> SIL
    MSK --> GL
    SIL --> GL --> GLD --> RS
    RS --> RECON & QS
    TMAPI -.-> RECON

    style SOURCES fill:#E1BEE7,stroke:#7B1FA2,stroke-width:2px
    style LAKE fill:#B3E5FC,stroke:#0277BD,stroke-width:2px
    style AWS fill:#E0E0E0,stroke:#424242,stroke-width:2px
    style OUT fill:#DCEDC8,stroke:#558B2F,stroke-width:3px
```

## AWS data stack (Phase 3)

| Service | Role |
|---------|------|
| **S3** | Legacy landing + medallion zones; Parquet; partition by COB / source |
| **Glue** | Legacy→TM transforms; crawlers; ongoing lake ETL |
| **Redshift** | Migration warehouse; GL facts; parity vs legacy |
| **MSK** | CDC / payment events after TM go-live |
| **QuickSight** | Cutover dashboards, recon sign-off |
| **IAM / KMS** | Least privilege; encryption at rest |

_Optional on specific programs:_ Step Functions, Iceberg migration DB, Athena recon — see `data-migration-infra-main/`._

## Key features (this repo)

| Feature | Location |
|---------|----------|
| **Legacy extractors** | `extractor.py`, `connector_base.py` — T24 / Finacle / Flexcube-style patterns |
| **Validation** | `validator.py` — row counts, schema checks |
| **TM mapping packs** | Documented in [docs/migration_phases.md](docs/migration_phases.md) |
| **Reference infra** | `data-migration-infra-main/` — Glue, Step Functions, Lambda (one program) |
| **Pipeline script map** | [docs/gft_migration_pipeline.md](docs/gft_migration_pipeline.md) |

## Project layout

```
gft-cloud-data-migration-framework/
├── connector_base.py
├── extractor.py
├── validator.py
├── data-migration-infra-main/   # Optional: Terraform + Glue reference (one program)
└── docs/
    ├── migration_phases.md
    └── gft_migration_pipeline.md
```

## Quick start

```bash
git clone https://github.com/willtran112358/gft-cloud-data-migration-framework.git
cd gft-cloud-data-migration-framework
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

See [docs/migration_phases.md](docs/migration_phases.md) for legacy→TM mapping examples.

---

**Will Tran** — [@willtran112358](https://github.com/willtran112358)
