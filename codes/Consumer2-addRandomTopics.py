from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
import random
import logging

# Kafka configuration
BOOTSTRAP_SERVERS = 'kafka1:29092'
INPUT_TOPIC = 'enriched_users_info_timestamp'
OUTPUT_TOPIC = 'enriched_users_info_randomtopics'

majors = [
    "Computer Science",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Biology",
    "Chemistry",
    "Physics",
    "Mathematics",
    "Psychology",
    "Business Administration",
    "Economics",
    "Marketing",
    "Finance",
    "English Literature",
    "History"
]


hobbies = [
    "Cooking",
    "Gardening",
    "Painting",
    "Hiking",
    "Running",
    "Singing",
    "Dancing",
    "Photography",
    "Fishing",
    "Yoga",
    "Reading",
    "Writing",
    "Cycling",
    "Knitting",
    "Woodworking"
]



consumer = KafkaConsumer(INPUT_TOPIC,
                        auto_offset_reset='earliest', # where to start reading the messages at
                        group_id='event-collector-group-2', # consumer group id
                        bootstrap_servers=['kafka1:29092'],
                        value_deserializer=lambda m: json.loads(m.decode('utf-8')) ,# we deserialize our data from json
                        security_protocol= 'PLAINTEXT'
                        )

producer = KafkaProducer(bootstrap_servers=['kafka1:29092'],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                        max_block_ms=5000)
def consume_and_enrich():
    print("Consumer 2 Started ...")

    for message in consumer:
        try:
            # Read the original message
            original_message = message.value
            
            # Add two random tags
            original_message['random_majors'] = random.choice(majors)
            original_message['random_hobbies'] = random.choice(hobbies)


            # Send the enriched message to the output topic
            producer.send(OUTPUT_TOPIC, value=original_message)

            print("Enriched message in producer 3 sent: id is {}".format(original_message["id"]))
        except Exception as e:
            logging.error(f'An error occured: {e}')




if __name__ == '__main__':
    consume_and_enrich()
