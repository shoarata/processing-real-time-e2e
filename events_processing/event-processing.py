import glob

from pyflink.table import TableEnvironment, EnvironmentSettings, TableDescriptor, Schema, DataTypes, FormatDescriptor
from config import settings
from loguru import logger
import os

table_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
jars = [f"file://{jar_path}" for jar_path in glob.glob(os.path.join(os.path.dirname(__file__), 'jars', "*"))]
logger.info(f"Using jars: {jars}")
table_env.get_config().set("pipeline.jars", ";".join(jars))
events_raw_schema = Schema.new_builder() \
    .column("event_time", DataTypes.TIMESTAMP(3)) \
    .column("event_type", DataTypes.STRING()) \
    .column("product_id", DataTypes.INT()) \
    .column("category_id", DataTypes.BIGINT()) \
    .column("category_code", DataTypes.STRING()) \
    .column("brand", DataTypes.STRING()) \
    .column("price", DataTypes.FLOAT()) \
    .column("user_id", DataTypes.BIGINT()) \
    .column("user_session", DataTypes.STRING()) \
    .column("ip", DataTypes.STRING()) \
    .watermark("event_time", "event_time - INTERVAL '5' SECOND") \
    .build()
table_env.create_temporary_table(
    path="ecommerce_events_raw",
    descriptor=TableDescriptor.for_connector("kafka").schema(events_raw_schema)
    .option("topic", settings.ECOMMERCE_TOPIC_NAME)
    .option("properties.bootstrap.servers", settings.KAFKA_CONFIG.bootstrap_servers)
    .option("properties.group.id", settings.CONSUMER_GROUP_ID)
    .option("scan.startup.mode", "earliest-offset")
    .format(FormatDescriptor.for_format("json").build())
    .build()
)

table_env.create_temporary_table(
    path="print_table",
    descriptor=TableDescriptor.for_connector("print").schema(events_raw_schema).build()
)
events_table = table_env.from_path("ecommerce_events_raw")
events_table.execute_insert("print_table").wait()

