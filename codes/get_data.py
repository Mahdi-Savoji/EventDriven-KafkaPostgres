import uuid
from datetime import datetime
import json
from kafka import KafkaProducer
import time
import logging

PRODUCER_TOPIC_NAME = "users_info"
def get_data():
    import requests

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]

    return res

def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():


    producer = KafkaProducer(bootstrap_servers=['kafka1:29092'], max_block_ms=5000)
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        try:
            res = get_data()
            res = format_data(res)
            
            producer.send(PRODUCER_TOPIC_NAME, json.dumps(res).encode('utf-8'))
            print('user_info sent from producer 1 : {}'.format(res['id'])) 
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue

if __name__ == '__main__':
    stream_data()
