# snowflake-dbt-pipeline

A cloud data modeling pipeline: S3 as the data lake, Snowflake as the warehouse, and dbt as the transformation layer.

## Status

End-to-end flow is working: CSVs land in S3, get copied into Snowflake raw tables, and dbt transforms them through bronze, silver, and gold layers, with SCD Type 2 dimension snapshots on top.

## Data

`source_data/` holds a synthetic Airbnb-style dataset used to build out the pipeline:

- `listings.csv` — property listings (property type, room type, location, pricing)
- `hosts.csv` — hosts who own listings
- `bookings.csv` — bookings made against listings

## Pipeline stages

1. **S3 ingestion** — `scripts/upload_to_s3.py` uploads the CSVs to `s3://snowflake-dbt-pp/raw-source-data/`.
2. **Snowflake warehouse setup** — `scripts/snowflake_warehouse_setup.py` (using the `snowflake.core` Python API) creates the `AIRBNB_PP` database, `STAGING` schema, and the `HOSTS`/`LISTINGS`/`BOOKINGS` raw tables, plus an external stage (`raw_s3_stage`) backed by a Snowflake storage integration that assumes an IAM role scoped to that S3 bucket/prefix — no long-lived AWS keys stored in Snowflake.
3. **Load** — `scripts/copy_into_snowflake.py` runs `COPY INTO` (via raw SQL, since file formats/loads aren't modeled as `snowflake.core` objects) to load the staged CSVs into the raw tables.
4. **Transform (dbt)** — the `airbnb_pipeline/` dbt project reads from `STAGING` and builds it up through bronze, silver, and gold layers:
   - **Bronze** (`models/bronze/`, incremental) — raw passthrough of `hosts`, `listings`, `bookings` from the `staging` source, watermarked incrementally on `created_at`.
   - **Silver** (`models/silver/`, incremental) — cleaned/derived versions of each bronze table: normalized host names, a response-rate quality bucket, a price-per-night tag (via the `classify` macro), and a computed `total_amount` per booking (via the `multiply` macro).
   - **Gold** (`models/gold/`) — `obt.sql` joins the three silver tables into a one-big-table view; `fact.sql` joins that OBT against the `DIM_LISTINGS`/`DIM_HOSTS` snapshot dimensions. `models/gold/ephemeral/` splits the OBT back into per-entity ephemeral models (`bookings`, `hosts`, `listings`) that feed the snapshots below.
   - **Snapshots** (`snapshots/`) — `dim_bookings`, `dim_hosts`, `dim_listings` use dbt's timestamp snapshot strategy (watermarked on `CREATED_AT`) to track slowly changing dimensions (SCD Type 2) in the `GOLD` schema.

## Project layout

```
source_data/                       Raw CSVs to be uploaded to S3
src/utils/s3_helpers.py            Reusable S3 helpers: create_bucket, upload_to_bucket
scripts/upload_to_s3.py            Uploads source_data/*.csv to S3
scripts/snowflake_warehouse_setup.py  Creates the Snowflake database/schema/tables/stage
scripts/copy_into_snowflake.py     Loads staged CSVs into Snowflake raw tables
airbnb_pipeline/                   dbt project: bronze/silver/gold models, snapshots, sources, macros
notebooks/                         Exploratory/prototype notebooks (gitignored, not versioned)
```

## Usage

Install dependencies and sync the project (editable install, so `src` is importable):

```
uv sync
```

Run the pipeline end to end:

```
uv run python -m scripts.upload_to_s3
uv run python scripts/snowflake_warehouse_setup.py
uv run python scripts/copy_into_snowflake.py
cd airbnb_pipeline && uv run dbt run && uv run dbt snapshot
```

AWS credentials come from the standard AWS credential chain (`~/.aws/credentials`, env vars, etc.); Snowflake auth uses key-pair (JWT) auth via `~/.snowflake/connections.toml`. No credentials are stored in this repo.

## Next steps

- Add dbt tests/documentation across bronze, silver, and gold models
- Schedule the pipeline (e.g. dbt Cloud, Airflow, or a cron-triggered script) instead of manual runs
