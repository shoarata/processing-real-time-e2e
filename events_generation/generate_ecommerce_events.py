import random
import time

import pandas as pd
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from config import settings
from datetime import datetime
from loguru import logger
import os


kafka_config = {
    "bootstrap.servers": settings.KAFKA_CONFIG.bootstrap_servers
}
logger.info(f"kafka config: {kafka_config}")

def create_topic_if_not_exists():
    kafka_admin = AdminClient(kafka_config)
    logger.info("Trying to create topic..")
    if settings.ECOMMERCE_TOPIC_NAME not in list(kafka_admin.list_topics().topics.keys()):
        logger.info(f"Topic not found in list {list(kafka_admin.list_topics().topics.keys())}, creating topic {settings.ECOMMERCE_TOPIC_NAME}")
        kafka_admin.create_topics(new_topics=[NewTopic(settings.ECOMMERCE_TOPIC_NAME)])
    else:
        logger.info(f"Topic {settings.ECOMMERCE_TOPIC_NAME} already exists.")

def log_produced_events(err, msg):
    if err:
        logger.error(f"failed to log event, {msg=}, {err=}")
    else:
        logger.info(f"success- msg logged to topic {msg.topic()}, {msg.value()=}")

def log_ecommerce_events():
    producer = Producer(kafka_config)
    logger.info("reading csv with events")
    events_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data", "events.csv"))
    logger.info("csv loaded")
    try:
        while True:
            i = random.randint(0, len(events_df) - 1)
            event = events_df.iloc[i]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            event["event_time"] = timestamp
            month = timestamp[:7]
            producer.produce(topic=settings.ECOMMERCE_TOPIC_NAME, value=event.to_json(), key=month, callback=log_produced_events)
            producer.poll(1)
            time.sleep(2)
    except KeyboardInterrupt:
        logger.info("keyboard interrupt, stopping...")

if __name__ == "__main__":
    create_topic_if_not_exists()
    log_ecommerce_events()
