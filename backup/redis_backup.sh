#!/bin/sh
date=`date +%Y%m%d`
backup=/home/ubuntu/backup

# Make new backups
tar -cvzf $backup/redis_db_backup_$date.tar.gz /var/redis/6379
tar -cvzf $backup/redis_config_backup_$date.tar.gz /etc/redis/redis_6379.conf
chown ubuntu:ubuntu $backup/redis*
chmod 640 $backup/redis*

# Delete backups older than 30 days
find $backup/redis* -mtime +30 -exec rm {} \;
