from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
import logging

# Kafka configuration
BOOTSTRAP_SERVERS = 'kafka1:29092'
INPUT_TOPIC = 'users_info'
OUTPUT_TOPIC = 'enriched_users_info_timestamp'

consumer = KafkaConsumer('users_info',
                        auto_offset_reset='earliest', # where to start reading the messages at
                        group_id='event-collector-group-1', # consumer group id
                        bootstrap_servers=['kafka1:29092'],
                        value_deserializer=lambda m: json.loads(m.decode('utf-8')) ,# we deserialize our data from json
                        security_protocol= 'PLAINTEXT'
                        )

producer = KafkaProducer(bootstrap_servers=['kafka1:29092'],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                        max_block_ms=5000)
def consume_and_enrich():
    print("Consumer 1 Started ...")

    for message in consumer:
        try:
            # Read the original message
            original_message = message.value
            
            # Add timestamp
            original_message['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Send the enriched message to the output topic
            producer.send(OUTPUT_TOPIC, value=original_message)

            print("Enriched message in producer 2 sent: id is {}".format(original_message["id"]))
        except Exception as e:
            logging.error(f'An error occured: {e}')

    

if __name__ == '__main__':
    consume_and_enrich()
