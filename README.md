# ThoughtMachine Banking Data Integration Platform

Enterprise data migration and ETL platform for ThoughtMachine Core Banking systems with cryptographic ledger support, change data capture, and regulatory compliance.

## Overview

Production-grade data integration platform for ThoughtMachine Core Banking migrations and analytics:
- **Source System**: ThoughtMachine Core Banking (Cryptography Module, General Ledger, Contracts, Customers)
- **Target Systems**: AWS (Redshift, RDS), Snowflake, Data Warehouse, Analytics Databases
- **Key Capabilities**: Schema detection, CDC streaming, data validation, reconciliation, lineage tracking
- **Use Cases**: Core system migrations, data lake ingestion, analytics warehouse builds, regulatory reporting

## Architecture

```mermaid
graph TB
    TM["🏦 ThoughtMachine<br/>Core Banking<br/>Vault • GL • Contracts<br/>Customers • Calendar"]
    
    TM --> TMAPI["📡 ThoughtMachine API<br/>REST/gRPC Connectors<br/>Streaming SDK"]
    
    TMAPI --> CDC["🔄 CDC Module<br/>Change Stream Capture<br/>Transaction Logs<br/>Ledger Changes"]
    
    CDC --> KAFKA["📨 Kafka Topics<br/>Ledger-transactions<br/>GL-balances<br/>Contract-changes<br/>Customer-updates"]
    
    KAFKA --> EXTRACT["✅ Extraction Layer<br/>Schema Detection<br/>Data Validation<br/>Duplicate Handling"]
    
    EXTRACT --> S3["☁️ S3 Staging<br/>Bronze (Raw)<br/>Silver (Cleaned)<br/>Parquet Format<br/>Partitioned"]
    
    S3 --> TRANSFORM["🔧 Transformation<br/>Schema Mapping<br/>Data Type Coercion<br/>Encryption Handling<br/>Key Derivation"]
    
    TRANSFORM --> VALIDATE["✔️ Validation Layer<br/>Row Count Check<br/>Checksum Verify<br/>Data Quality Rules<br/>Regex Patterns"]
    
    VALIDATE --> TARGET["🎯 Target Systems<br/>AWS Redshift<br/>RDS PostgreSQL<br/>Snowflake<br/>Data Warehouse"]
    
    VALIDATE --> RECONCILE["🔍 Reconciliation<br/>Source vs Target<br/>Discrepancy Report<br/>Auto-remediation"]
    
    RECONCILE --> AUDIT["📋 Audit Trail<br/>Data Lineage<br/>Transformation History<br/>Compliance Logs"]
    
    AIRFLOW["⚙️ Airflow<br/>DAG Orchestration<br/>Error Handling<br/>Retry Logic"] -.-> TMAPI
    AIRFLOW -.-> EXTRACT
    AIRFLOW -.-> TRANSFORM
    AIRFLOW -.-> VALIDATE
    
    MONITOR["📊 Monitoring<br/>Prometheus<br/>ELK Stack<br/>CloudWatch"] -.-> KAFKA
    MONITOR -.-> VALIDATE
    MONITOR -.-> TARGET
    
    style TM fill:#1a5490,stroke:#000,color:#fff
    style TMAPI fill:#2E7D32,stroke:#000,color:#fff
    style CDC fill:#0097A7,stroke:#000,color:#fff
    style KAFKA fill:#FF6F00,stroke:#000,color:#fff
    style TARGET fill:#7B1FA2,stroke:#000,color:#fff
    style AUDIT fill:#F57F17,stroke:#000,color:#fff
```

## Key Features

| Feature | Description |
|---------|-------------|
| **ThoughtMachine Integration** | Direct API integration with Core Banking GL, cryptography, contracts |
| **CDC Streaming** | Real-time change capture with Kafka topics for ledger transactions |
| **Schema Auto-Detection** | Automatic discovery of GL account hierarchy, contract structure |
| **Data Transformation** | GL account mapping, encrypted field handling, format conversion |
| **Validation Framework** | Row count reconciliation, checksum verification, business rules |
| **Multi-Target Support** | AWS Redshift, RDS, Snowflake, custom data warehouses |
| **Audit & Lineage** | Complete data provenance, transformation history, compliance logs |
| **Error Recovery** | Retry logic, dead-letter queues, manual intervention workflows |
| **Performance** | Parallel extraction, batching (10K+ rows/sec), connection pooling |

## Quick Start

```bash
git clone https://github.com/willtran112358/thoughtmachine-data-migration.git
cd thoughtmachine-data-migration

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with TM_API credentials and target DB

# Run migration
python src/migrate.py --source thoughtmachine --target redshift

# Or use Airflow
airflow dags trigger thoughtmachine_bank_etl
```

## Testing

```bash
pytest tests/unit -v
pytest tests/integration --markers integration
```

## Contributing

1. Create feature branch
2. Add tests (85%+ coverage)
3. Submit PR

## License

MIT License

## Author

**WillTran** — [@willtran112358](https://github.com/willtran112358)