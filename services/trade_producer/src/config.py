import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

kafka_broker_address = os.environ['KAFKA_BROKER_ADDRESS']
kafka_topic_name = 'trade'
product_id = 'BTC/USD'
