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
    .build()

ip_location_schema = Schema.new_builder()\
    .column("ip_from", DataTypes.BIGINT()) \
    .column("ip_to", DataTypes.BIGINT()) \
    .column("country_code", DataTypes.STRING()) \
    .column("country_name", DataTypes.STRING()) \
    .build()