#!/bin/sh
date=`date +%Y%m%d`
backup=/home/ubuntu/backup

# Make new backups of crack
tar -cvzf $backup/crack_backup_$date.tar.gz /var/www/crack
chown ubuntu:ubuntu $backup/crack* 
chmod 640 $backup/crack*

# Make new backups of the database
tar -cvzf $backup/redis_backup_$date.tar.gz /var/redis/6379
chown ubuntu:ubuntu $backup/redis*
chmod 640 $backup/redis*

# Delete backups older than 30 days
find $backup/crack* -mtime +30 -exec rm {} \;
find $backup/redis* -mtime +30 -exec rm {} \;
