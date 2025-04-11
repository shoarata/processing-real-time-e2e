import random

import pandas as pd
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer
from config import settings
from datetime import datetime
from loguru import logger
import os

def create_topic_if_not_exists():
    kafka_admin = AdminClient(settings.kakfa_config)
    if settings.ecommerce_topic_name not in list(kafka_admin.list_topics().topics.keys()):
        kafka_admin.create_topics(new_topics=[settings.ecommerce_topic_name])

def log_ecommerce_events():
    producer = Producer(settings.kakfa_config)
    events_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data", "events.csv"))
    try:
        while True:
            i = random.randint(0, len(events_df) - 1)
            event_dct = events_df.iloc[i].to_dict()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%s")
            event_dct["event_time"] = timestamp
            month = timestamp[:7]
            producer.produce(topic=settings.ecommerce_topic_name, value=event_dct, key=month)
    except KeyboardInterrupt:
        logger.info("keyboard interrupt, stopping...")






