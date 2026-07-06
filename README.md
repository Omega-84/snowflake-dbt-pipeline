# snowflake-dbt-pipeline

A cloud data modeling pipeline: S3 as the data lake, Snowflake as the warehouse, and dbt as the transformation layer.

## Status

Currently at the **S3 ingestion** stage — raw CSVs are uploaded from local storage to S3. Snowflake stage/warehouse setup and dbt models have not been built yet.

## Data

`source_data/` holds a synthetic Airbnb-style dataset used to build out the pipeline:

- `listings.csv` — property listings (property type, room type, location, pricing)
- `hosts.csv` — hosts who own listings
- `bookings.csv` — bookings made against listings

## Project layout

```
source_data/            Raw CSVs to be uploaded to S3
src/utils/s3_helpers.py Reusable S3 helpers: create_bucket, upload_to_bucket
scripts/upload_to_s3.py Entrypoint that creates the bucket and uploads all CSVs
notebooks/               Exploratory/prototype notebooks (gitignored, not versioned)
```

## Usage

Install dependencies and sync the project (editable install, so `src` is importable):

```
uv sync
```

Upload the CSVs in `source_data/` to S3 (creates the bucket if it doesn't exist):

```
uv run scripts/upload_to_s3.py
```

This uploads each CSV to `s3://snowflake-dbt-pp/raw-source-data/<filename>.csv`. AWS credentials are picked up from the standard AWS credential chain (`~/.aws/credentials`, environment variables, etc.) — no credentials are stored in this repo.

## Next steps

- Set up a Snowflake external stage / storage integration pointing at the S3 bucket
- Scaffold a dbt project and build staging/mart models on top of the raw data
