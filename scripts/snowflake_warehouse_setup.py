from snowflake.core import CreateMode, Root
from snowflake.snowpark import Session
from snowflake.core.database import Database
from snowflake.core.schema import Schema
from snowflake.core.table import Table, TableColumn, PrimaryKey

session = Session.builder.config("connection_name", "default").create()
root = Root(session)

DATABASE_NAME = "AIRBNB_PP"
SCHEMA_NAME = "STAGING"
HOST_TABLE_NAME = 'HOSTS'
LISTINGS_TABLE_NAME = 'LISTINGS'
BOOKINGS_TABLE_NAME = 'BOOKINGS'

my_db = Database(name=DATABASE_NAME)
root.databases.create(my_db, mode=CreateMode.if_not_exists)

my_schema = Schema(name=SCHEMA_NAME)
root.databases[DATABASE_NAME].schemas.create(my_schema, mode=CreateMode.if_not_exists)

host_table = Table(
  name=HOST_TABLE_NAME,
  columns=[TableColumn(name="host_id", datatype="int", constraints=[PrimaryKey()]),
           TableColumn(name="host_name", datatype="string"),
           TableColumn(name="host_since", datatype="date"),
           TableColumn(name="is_superhost", datatype="boolean"),
           TableColumn(name="response_rate", datatype="int"),
           TableColumn(name="created_at", datatype="timestamp_ntz"),
           ]
)
root.databases[DATABASE_NAME].schemas[SCHEMA_NAME].tables.create(host_table, mode=CreateMode.if_not_exists)


listings_table = Table(
  name=LISTINGS_TABLE_NAME,
  columns=[TableColumn(name="listing_id", datatype="int", constraints=[PrimaryKey()]),
           TableColumn(name="host_id", datatype="int"),
           TableColumn(name="property_type", datatype="string"),
           TableColumn(name="room_type", datatype="string"),
           TableColumn(name="city", datatype="string"),
           TableColumn(name="country", datatype="string"),
           TableColumn(name="accommodates", datatype="int"),
           TableColumn(name="bedrooms", datatype="int"),
           TableColumn(name="bathrooms", datatype="int"),
           TableColumn(name="price_per_night", datatype="int"),
           TableColumn(name="created_at", datatype="timestamp_ntz"),
           ]
)
root.databases[DATABASE_NAME].schemas[SCHEMA_NAME].tables.create(listings_table, mode=CreateMode.if_not_exists)

bookings_table = Table(
  name=BOOKINGS_TABLE_NAME,
  columns=[TableColumn(name="booking_id", datatype="string", constraints=[PrimaryKey()]),
           TableColumn(name="listing_id", datatype="int"),
           TableColumn(name="booking_date", datatype="timestamp_ntz"),
           TableColumn(name="nights_booked", datatype="int"),
           TableColumn(name="booking_amount", datatype="int"),
           TableColumn(name="cleaning_fee", datatype="int"),
           TableColumn(name="service_fee", datatype="int"),
           TableColumn(name="booking_status", datatype="string"),
           TableColumn(name="created_at", datatype="timestamp_ntz"),
           ]
)
root.databases[DATABASE_NAME].schemas[SCHEMA_NAME].tables.create(bookings_table, mode=CreateMode.if_not_exists)

