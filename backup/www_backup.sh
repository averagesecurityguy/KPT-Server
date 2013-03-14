#!/bin/sh
date=`date +%Y%m%d`
backup=/home/ubuntu/backup

# Make new backups of crack
tar -cvzf $backup/crack_backup_$date.tar.gz /var/www/crack /usr/lib/python2.7/server_oauth.py /usr/lib/python2.7/crack_db.py
chown ubuntu:ubuntu $backup/crack* 
chmod 640 $backup/crack*

# Delete backups older than 30 days
find $backup/crack* -mtime +30 -exec rm {} \;
