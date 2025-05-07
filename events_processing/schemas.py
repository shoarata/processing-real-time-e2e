from pyflink.table import Schema, DataTypes

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

ip_location_csv_schema ={
    "ip_from": int,
    "ip_to": int,
    "country_code": str,
    "country_name": str
}

enriched_events_schema = Schema.new_builder() \
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
    .column("event_date", DataTypes.STRING()) \
    .column("event_hour", DataTypes.STRING()) \
    .column("event_minute", DataTypes.STRING()) \
    .column("country_code", DataTypes.STRING()) \
    .build()
