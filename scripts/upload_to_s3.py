import logging
import sys
from pathlib import Path

from src.utils import create_bucket, upload_to_bucket

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

BUCKET_NAME = "snowflake-dbt-pp"
DIRECTORY_NAME = "raw-source-data"
SOURCE_DATA = Path(__file__).resolve().parent.parent / "source_data"

try:
    create_bucket(bucket_name=BUCKET_NAME)
    logger.info("Bucket %s succesfully created", BUCKET_NAME)
except Exception as e:
    sys.exit(f"Bucket not created because of {e}")

csv_files = sorted(SOURCE_DATA.glob("*.csv"))

for file in csv_files:
    try:
        upload_to_bucket(str(file), BUCKET_NAME, f"{DIRECTORY_NAME}/{file.name}")
        logger.info("%s uploaded successfully to %s", file.name, BUCKET_NAME)
    except Exception as e:
        logger.error("%s was not uploaded due to %s", file.name, e)