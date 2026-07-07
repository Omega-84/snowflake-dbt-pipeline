import logging

import snowflake.connector

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

conn = snowflake.connector.connect(connection_name='default')

cur = conn.cursor()

DATABASE_NAME = "AIRBNB_PP"
SCHEMA_NAME = "STAGING"
HOST_TABLE_NAME = 'HOSTS'
LISTINGS_TABLE_NAME = 'LISTINGS'
BOOKINGS_TABLE_NAME = 'BOOKINGS'
STAGE_NAME = 'raw_s3_stage'

cur.execute(f"USE DATABASE {DATABASE_NAME}")
cur.execute(f"USE SCHEMA {SCHEMA_NAME}")

cur.execute("""
            CREATE FILE FORMAT IF NOT EXISTS csv_format
            TYPE = 'CSV' 
            FIELD_DELIMITER = ','
            SKIP_HEADER = 1
            ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;
            """)

cur.execute(
            f"""
            COPY INTO {HOST_TABLE_NAME}
            FROM @{STAGE_NAME}
            FILE_FORMAT = (FORMAT_NAME = 'csv_format')
            FILES=('hosts.csv')
            """)
logger.info("hosts.csv copy result: %s", cur.fetchall())

cur.execute(
            f"""
            COPY INTO {LISTINGS_TABLE_NAME}
            FROM @{STAGE_NAME}
            FILE_FORMAT = (FORMAT_NAME = 'csv_format')
            FILES=('listings.csv')
            """)
logger.info("listings.csv copy result: %s", cur.fetchall())

cur.execute(
            f"""
            COPY INTO {BOOKINGS_TABLE_NAME}
            FROM @{STAGE_NAME}
            FILE_FORMAT = (FORMAT_NAME = 'csv_format')
            FILES=('bookings.csv')
            """)
logger.info("bookings.csv copy result: %s", cur.fetchall())

cur.close()
conn.close()