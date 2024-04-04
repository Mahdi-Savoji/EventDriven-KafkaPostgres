

# Event-Driven Data Processing with Kafka, PostgreSQL, and Python



## Python file

#### get_data

- **Purpose**:
  - This Python script utilizes the Kafka library to continuously stream randomly generated user information to a Kafka topic named "users_info". The script defines functions to fetch data from a random user API and format it into a dictionary with specific keys representing user attributes. Within a loop, the script creates a Kafka producer and sends the formatted user data to the specified topic in JSON format. Error handling is implemented to log any exceptions that occur during data streaming. When executed, the script runs indefinitely, periodically fetching new user data and sending it to the Kafka topic until manually terminated.

- **Consumer2-addRandomTopics**:
  - This Python script acts as a Kafka consumer, listening to messages from the "users_info" topic, enriches each message with a timestamp, and then sends the enriched message to another Kafka topic named "enriched_users_info_timestamp". The script sets up a Kafka consumer with specified configurations such as bootstrap servers, auto offset reset, and deserialization of JSON data. It also configures a Kafka producer to send messages with JSON serialization. Within the main function `consume_and_enrich()`, it iterates over messages received from the consumer, enriches each message with the current timestamp, and sends the enriched message to the output topic via the producer. Error handling is implemented to log any exceptions that occur during message processing. Upon execution, the script continuously consumes and enriches messages from the input topic until terminated manually.

- **Consumer2-addRandomTopics**:
  -  This Python script functions as a Kafka consumer, processing messages from the "enriched_users_info_timestamp" topic, enriches each message with two randomly selected tags from predefined lists of majors and hobbies, and then sends the enriched message to the "enriched_users_info_randomtopics" topic. The script defines lists of majors and hobbies, sets up a Kafka consumer with specified configurations such as bootstrap servers, auto offset reset, and deserialization of JSON data. It also configures a Kafka producer to send messages with JSON serialization. Within the main function `consume_and_enrich()`, it iterates over messages received from the consumer, adds two random tags to each message, and sends the enriched message to the output topic via the producer. Error handling is implemented to log any exceptions that occur during message processing. Upon execution, the script continuously consumes and enriches messages from the input topic until terminated manually.

- **Consumer3-SaveInPostgres**:
  - This Python script serves as a Kafka consumer, responsible for processing messages from the "enriched_users_info_randomtopics" topic, and then persisting the data into a PostgreSQL database. The script defines a SQLAlchemy ORM model called `User` with attributes representing various user information. It sets up a Kafka consumer with specified configurations, such as bootstrap servers and deserialization of JSON data. Additionally, it configures a connection to a PostgreSQL database using SQLAlchemy, and creates a session for interacting with the database. Within the `consume_and_save_to_database()` function, it iterates over messages received from the Kafka consumer, creates `User` objects with the extracted data, and adds them to the database session for persistence. Error handling is implemented to log any exceptions that occur during message processing. Upon execution, the script continuously consumes messages from the input topic and saves user data to the PostgreSQL database until manually terminated.

## Docker

#### Postgresql

- **Purpose**: 
  
  - This service is responsible for storing data from the last consumer in Kafka into PostgreSQL.
  
- **Usage Tips**:
  
  1. **Backup Configuration**:
     
     - In the provided directory, there's a `postgresql.conf` file. To enable WAL (Write Ahead Log) archiving for backup, move this file to the `db_data` folder and make necessary configuration changes.
     
  2. **Full Backup**:
     
     - To perform a full database backup, uncomment the relevant code in the Docker Compose file and make sure to use the provided Dockerfile and backup scripts for scheduled backups.
     
     - cronjob-backup.sh file:
     
       This Bash script configures a cron job to execute a backup script weekly, specifically on Saturdays at 2 AM. It creates the cron job configuration file, grants execution permissions, and sets up logging for cron job activities. The script then starts the cron service and ensures continuous execution by running indefinitely with the tail command. 
     
     - backup-weekly.sh file:
     
       This Bash script is designed to take a PostgreSQL base backup using the `pg_basebackup` command. It begins by attempting to switch to the "postgres" user, followed by executing the backup command with options specifying the backup directory (`$BACKUP_DIR`) and backup mode (`fast`). However, the script's use of `su postgres` may not function as intended due to subsequent commands being executed by the original user. It's crucial to ensure proper authentication and permissions for executing the script, particularly when executed non-interactively, such as through a cron job.

#### Nocodb 

If you want to use nocodb instead of the PostgreSQL service, you should uncomment the nocodb service and comment out the PostgreSQL service in the Docker Compose file. Then, you need to bring up the Docker Compose environment again.

#### Zookeeper

- **Purpose**:
  - This service plays a crucial role in coordinating distributed systems, including Kafka.

#### Kafka1

- **Purpose**:
  - This service is essential for managing streaming events within the system.

- **Usage Tips**:
  1. **Network Configuration**:
     - If Kafka1 is intended to be used in another network, ensure to add `127.0.0.1 kafka1` to the hosts file in your operating system.

#### KafkaHQ

- **Purpose**:
  - The KafkaHQ service is deployed to monitor Kafka performance through a graphical user interface (GUI). However, in this project, it is not utilized to create or manage topics automatically.     

#### Ubun2

- **Purpose**:
  - The Ubuntu service is utilized to manage the execution of Python scripts that mount volume codes directory with this container, fetching data, and sending it to Kafka nodes. It utilizes a cronjob that runs the `get_data.py` file every minute.

    - script_manager.sh file for timing call get_data.py:
  
      This Bash script orchestrates the execution of Python scripts for data processing and scheduling tasks. Initially, it navigates to a directory, waits for a minute, and then launches four Python scripts concurrently. Additionally, it sets up a cron job to run one of the Python scripts every minute, with logging enabled. Finally, it ensures the continuous operation of the script by keeping it running indefinitely in the foreground. This script effectively automates data processing and scheduling activities.
  

## Usage

To run this project, install Docker Engine in the project directory and execute the following command:

```
docker compose -f ./dockercompose up
```

**Note**: Pay attention to Backup Configuration and Full Backup sections in the PostgreSQL part, which explain how to set up backup configurations and perform full backups to save Write Ahead Log (WAL) files if necessary.