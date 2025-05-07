import glob
import ipaddress
import os

import pandas as pd
from loguru import logger
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableDescriptor, DataTypes, FormatDescriptor, StreamTableEnvironment
from pyflink.table.expressions import col, date_format
from pyflink.table.udf import udf

from config import settings
from schemas import events_raw_schema, enriched_events_schema, ip_location_csv_schema

env = StreamExecutionEnvironment.get_execution_environment()
env.enable_checkpointing(1000)

env_settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
table_env = StreamTableEnvironment.create(env, environment_settings=env_settings)

jars = [f"file://{jar_path}" for jar_path in glob.glob(os.path.join(os.path.dirname(__file__), 'jars', "*"))]
logger.info(f"Using jars: {jars}")
table_env.get_config().set("pipeline.jars", ";".join(jars))

ECOMMERCE_EVENTS_TABLE_NAME = "ecommerce_events_raw"
table_env.create_temporary_table(
    path=ECOMMERCE_EVENTS_TABLE_NAME,
    descriptor=TableDescriptor.for_connector("kafka").schema(events_raw_schema)
    .option("topic", settings.ECOMMERCE_TOPIC_NAME)
    .option("properties.bootstrap.servers", settings.KAFKA_CONFIG.bootstrap_servers)
    .option("properties.group.id", settings.CONSUMER_GROUP_ID)
    .option("scan.startup.mode", "group-offsets")
    .option("properties.auto.offset.reset", "earliest")
    .format(FormatDescriptor.for_format("json").build())
    .build()
)

events_table = table_env.from_path(ECOMMERCE_EVENTS_TABLE_NAME)
events_table = events_table.add_columns(date_format(col("event_time"), "yyyy-MM-dd").alias("event_date")) \
    .add_columns(date_format(col("event_time"), "HH").alias("event_hour")) \
    .add_columns(date_format(col("event_time"), "mm").alias("event_minute"))

ip_to_location_df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "IP2LOCATION-LITE-DB1.CSV"),
    names=ip_location_csv_schema,
    dtype=ip_location_csv_schema
)
@udf(result_type=DataTypes.STRING())
def ip_to_country_code(ip_str):
    dec_ip = int(ipaddress.IPv4Address(ip_str))
    match = ip_to_location_df[(ip_to_location_df["ip_from"] <= dec_ip) & (ip_to_location_df["ip_to"] >= dec_ip)]
    return match.iloc[0]["country_code"] if len(match) > 0 else ""

enriched_events_table = events_table.add_columns(ip_to_country_code(col("ip")).alias("country_code"))
ENRICHED_ECOMMERCE_EVENTS_TABLE_NAME = "ecommerce_platform_events"
enriched_events_table.print_schema()
table_env.create_table(
    path=ENRICHED_ECOMMERCE_EVENTS_TABLE_NAME,
    descriptor=TableDescriptor.for_connector("filesystem")
    .schema(enriched_events_schema)
    .option("path", settings.LOCAL_EVENTS_URI)
    .option("sink.partition-commit.trigger", 'process-time')
    .option("sink.partition-commit.policy.kind", "success-file")
    .format("parquet")
    .partitioned_by("event_date", "event_hour", "event_minute")
    .build()
)
enriched_events_table.execute_insert(table_path_or_descriptor=ENRICHED_ECOMMERCE_EVENTS_TABLE_NAME).wait()


