# GFT migration phases — legacy core → ThoughtMachine → AWS

For the **implemented AWS pipeline** (PostgreSQL → S3 → Glue staging → Iceberg migration → Lambda/Athena recon → ThoughtMachine), see **[gft_migration_pipeline.md](gft_migration_pipeline.md)** and `data-migration-infra-main/`.

## Phase 1: Legacy extract to S3

**Goal:** Freeze and land authoritative legacy snapshots before any ThoughtMachine load.

| Legacy system | Example entities | S3 prefix (illustrative) |
|---------------|------------------|---------------------------|
| **Temenos T24** | `CUSTOMER`, `AA_ARRANGEMENT`, `STMT_ENTRY`, GL tables | `s3://bank-migration/legacy/t24/cob_date=YYYY-MM-DD/` |
| **Finacle** | CIF, account master, transaction history, GL | `s3://bank-migration/legacy/finacle/` |
| **FLEXCUBE** | Customer, account, collateral, GL | `s3://bank-migration/legacy/flexcube/` |

**Practices**

- Partition by **COB date** / extract batch id.
- Store **manifest** (table, row count, checksum) alongside each drop.
- No TM API calls in this phase — read-only from legacy.

## Phase 2: ETL + ThoughtMachine mapping & load

**Goal:** Transform legacy-shaped files into **Vault-compatible** payloads and load TM so core features (accounts, contracts, balances, postings) are usable.

```
S3 legacy bronze
    → Glue Spark / Python ETL (this repo: extractor + validator patterns)
    → TM mapping layer (GFT packs: customer_id, product_id, denomination, flags)
    → TM staging tables / files
    → ThoughtMachine bulk ingest or API load
```

**Example mapping (illustrative)**

| Legacy (T24-style) | ThoughtMachine concept | Notes |
|--------------------|------------------------|-------|
| `CUSTOMER.NO` | `customer.id` | Stable external id |
| `AA product**` | `contract.product_version_id` | Product catalogue mapping table |
| GL balance snapshot | `balance` / posting migration | Cutover balance events |
| Open loans / deposits | `contract` create + schedules | Validated against TM product defs |

**Validation gates**

- Row counts: legacy extract = mapped output = TM acceptance report.
- Business rules: currency, status, closed accounts excluded per cutover policy.
- Failed rows → quarantine prefix on S3 for manual repair.

Only after **Phase 2** succeeds does ThoughtMachine hold the bank’s migrated core data.

## Phase 3: AWS analytics, CDC, and cutover

**Goal:** Operate parallel run and decommission legacy.

| Stream | Source | AWS target |
|--------|--------|------------|
| Ongoing vault events | ThoughtMachine API / streaming | MSK → S3 silver → Glue → Redshift |
| Legacy parity | S3 legacy snapshots | Redshift recon marts |
| Sign-off BI | Redshift marts | QuickSight dashboards |

**Reconciliation**

- **Legacy S3** vs **TM vault** vs **Redshift** — daily during parallel run.
- Mismatch thresholds drive cutover go/no-go.

## ThoughtMachine vs AWS ordering

```text
[ T24 | Finacle | FLEXCUBE ]  →  S3 legacy  →  mapping ETL  →  ThoughtMachine Vault
                                                                    ↓
                                              S3 gold / MSK / Glue / Redshift / QuickSight
```

This ordering matches how **GFT** runs APAC **ThoughtMachine** programs: cloud data stack supports migration and BAU **after** legacy data has been mapped into Vault.
