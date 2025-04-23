import glob
import ipaddress

from pyflink.table import TableEnvironment, EnvironmentSettings, TableDescriptor, Schema, DataTypes, FormatDescriptor
from pyflink.table.udf import udf
from pyflink.table.expressions import col
from config import settings
from loguru import logger
from schemas import events_raw_schema, ip_location_schema
import os


table_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
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
    .option("scan.startup.mode", "earliest-offset")
    .format(FormatDescriptor.for_format("json").build())
    .build()
)
IP_TABLE_NAME = "ip_location"
table_env.create_temporary_table(
    path=IP_TABLE_NAME,
    descriptor=TableDescriptor.for_connector("filesystem").schema((ip_location_schema))
    .option("path", os.path.join(os.path.dirname(__file__), "IP2LOCATION-LITE-DB1.CSV"))
    .format("csv")
    .build()
)
events_table = table_env.from_path(ECOMMERCE_EVENTS_TABLE_NAME)
ip_table = table_env.from_path(IP_TABLE_NAME)

@udf(result_type=DataTypes.BIGINT())
def ip_str_to_ip_dec(ip_str):
    return int(ipaddress.IPv4Address(ip_str))

enriched_events_table = events_table.add_columns(ip_str_to_ip_dec(col("ip")).alias("dec_ip"))
enriched_events_table = enriched_events_table.join(ip_table).where(col("dec_ip").between(col("ip_from"), col("ip_to")))
enriched_events_table = enriched_events_table.drop_columns(
    col("ip_from"),
    col("dec_ip"),
    col("ip_to"),
    col("country_name")
)
enriched_events_table.print_schema()
enriched_events_table.execute().print()



