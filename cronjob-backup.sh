#!/bin/bash

# Add the cron job to run the backup script every week (on saturday at 2 AM)
echo "0 2 * * 6 root /bin/bash /pg-docker/backup-weekly.sh" > /etc/cron.d/backup-weekly

# Give execution rights on the cron job
chmod 0644 /etc/cron.d/backup-weekly

# Create the log file to be able to run tail
touch /var/log/cron.log

# Start the cron service
cron -f &

# Keep the script running
tail -f /dev/null
