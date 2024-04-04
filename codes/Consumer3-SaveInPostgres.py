from kafka import KafkaConsumer
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

# Change the import statement for declarative_base
# Define SQLAlchemy ORM model
Base = declarative_base()

class User(Base):
    __tablename__ = 'random_users'

    id = Column(String, primary_key=True) 
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    address = Column(String)
    post_code = Column(String)
    email = Column(String)
    username = Column(String)
    dob = Column(DateTime)  
    registered_date = Column(DateTime)
    phone = Column(String)
    picture = Column(String)
    majors = Column(String)
    hobbies = Column(String)
    

# Kafka configuration
BOOTSTRAP_SERVERS = 'kafka1:29092'
INPUT_TOPIC = 'enriched_users_info_randomtopics'

consumer = KafkaConsumer(INPUT_TOPIC,
                        auto_offset_reset='earliest', # where to start reading the messages at
                        group_id='event-collector-group-3', # consumer group id
                        bootstrap_servers=['kafka1:29092'],
                        value_deserializer=lambda m: json.loads(m.decode('utf-8')) ,# we deserialize our data from json
                        security_protocol= 'PLAINTEXT'
                        )


# PostgreSQL configuration
DATABASE_URL = 'postgresql://postgres:postgres123@postgres:5432/dblab'  # Use service name instead of localhost


# Create database engine
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()


def consume_and_save_to_database():

    print("Consumer 3 Started ...")
    for message in consumer:
        try:
            # Read the original message
            user_data = message.value
            
            # Create User object
            user = User(id=user_data['id'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        email=user_data['email'],
                        gender = user_data['gender'],
                        address = user_data['address'],
                        post_code = user_data['post_code'],
                        username = user_data['username'],
                        dob = user_data['dob'],
                        registered_date = user_data['registered_date'],
                        phone = user_data['phone'],
                        picture = user_data['picture'],
                        majors = user_data['random_majors'],
                        hobbies = user_data['random_hobbies']
                        )

            # Add user to the database
            session.add(user)
            session.commit()

            print(f"User saved to database: {user.first_name} {user.last_name}")
        except Exception as e:
            logging.error(f'An error occured: {e}')

if __name__ == '__main__':
    consume_and_save_to_database()