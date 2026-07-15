CREATE STORAGE INTEGRATION s3_int
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = S3
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::310342906701:role/snowflake-s3-role'
    STORAGE_ALLOWED_LOCATIONS = ('s3://snowflake-dbt-pp/raw-source-data/');

DESC INTEGRATION S3_INT;

CREATE STAGE raw_s3_stage
  URL = 's3://snowflake-dbt-pp/raw-source-data/'
  STORAGE_INTEGRATION = s3_int;

LIST @raw_s3_stage;