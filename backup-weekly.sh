#!/bin/bash

su postgres
pg_basebackup -D "$BACKUP_DIR/standalone-$(date +%Y-%m-%dT%H-%M)" -c fast -P -R
