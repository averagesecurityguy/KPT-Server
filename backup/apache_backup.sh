#!/bin/sh
date=`date +%Y%m%d`
backup=/home/ubuntu/backup

# Make new backups
tar -cvzf $backup/apache_backup_$date.tar.gz /etc/apache2
tar -cvzf $backup/apache_log_backup_$date.tar.gz /var/log/apache2
chown ubuntu:ubuntu $backup/apache*
chmod 640 $backup/apache*

# Delete backups older than 30 days
find $backup/apache* -mtime +30 -exec rm {} \;
