#!/bin/bash

cd codes
sleep 60
python3 get_data.py & python3 Consumer1-addtTimeStamp.py & python3 Consumer2-addRandomTopics.py & python3 Consumer3-SaveInPostgres.py

# Add the cron job to run get_data.py every minute
echo "* * * * * root /usr/bin/python3 /codes/get_data.py" > /etc/cron.d/cronjob

# Give execution rights on the cron job
chmod 0644 /etc/cron.d/cronjob

# Create the log file to be able to run tail
touch /var/log/cron.log

# Start the cron service
cron -f &

# Keep the script running
tail -f /dev/null