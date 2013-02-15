# Database Schema
## Hash Databases
hash:{"plain": plaintext, "count": count}

## User Database
email: calculated_consumer_key
calculated_consumer_key:cracked_count: number
calculated_consumer_key:consumer_key: string
calculated_consumer_key:access_token: string
calculated_consumer_key:consumer_secret: string
calculated_consumer_key:access_token_secret: string
calculated_consumer_key:expiration: time in seconds
calculated_consumer_key:hash_count: number
calculated_consumer_key:email: email address

#Build Instructions
These instructions are for Ubuntu 12.04

## Install OS Dependencies
	* sudo apt-get install build-essential python-dev python-pip apache2 
	* sudo apt-get install libapache2-mod-wsgi git tcl

## Install Python Dependencies
    * pip install requests, smbpasswd, web.py, redis

## Install Software
	* git install https://github.com/averagesecurityguy/crackit
	* mkdir /var/www/crack
	* copy server.py static, and templates to /var/www/crack
	* copy crack_db.py server_oauth.py to /usr/lib/python2.7

## Configure Apache
	* Copy the apache config files to /etc/apache2/sites-available
	* Add the knownplaintext_co.crt, PositiveSSLCA2.crt, and AddTrustExternalCARoot.crt to /etc/ssl/certs
	* Add the knownplaintext.key to /etc/ssl/private
	* Enable mod_rewrite a2enmod rewrite
	* Enable mod_ssl a2enmod ssl
	* Disable the default site a2dissite default
	* Enable the sites a2ensite crack, a2ensite crack-ssl
    * Restart the Apache server

## Install Redis Server
	* Download the latest versio of Redis server: http://redis.googlecode.com/files/redis-2.6.10.tar.gz
	* Extract it tar -xvzf redis-2.6.10.tar.gz
	* cd redis-2.6.10/src
	* make
	* make test
	* cp redis-server redis-cli /usr/local/bin


## Configure Redis Server
	* Create /etc/redis and /var/redis
	* cp utils/redis_init_script /etc/init.d/redis_6379
	* sudo update-rc.d redis_6379 defaults
	* Copy the redis config file from the crackit repo to /etc/redis/
	* sudo mkdir /var/redis/6379

## Test the server
	* Start the server: /etc/init.d/redis_6379 start
	* Run redis-cli and do a save
	* Ensure the log file and db are saved properly

## Configure backup
	* Copy backup scripts to home directory of backup user
	* Setup cron job to run the scripts

	

Edit the configuration file, making sure to perform the following changes:
Set daemonize to yes (by default it is set to no).
Set the pidfile to /var/run/redis_6379.pid (modify the port if needed).
Change the port accordingly. In our example it is not needed as the default port is already 6379.
Set your preferred loglevel.
Set the logfile to /var/log/redis_6379.log
Set the dir to /var/redis/6379 (very important step!)
Finally add the new Redis init script to all the default runlevels using the following command:
sudo update-rc.d redis_6379 defaults
You are done! Now you can try running your instance with:
/etc/init.d/redis_6379 start
Make sure that everything is working as expected:
Try pinging your instance with redis-cli.
Do a test save with redis-cli save and check that the dump file is correctly stored into /var/redis/6379/ (you should find a file called dump.rdb).
Check that your Redis instance is correctly logging in the log file.
If it's a new machine where you can try it without problems make sure that after a reboot everything is still working.



* Copy the init script that you'll find in the Redis distribution under the utils directory into /etc/init.d. We suggest calling it with the name of the port where you are running this instance of Redis. For example:
sudo cp utils/redisinitscript /etc/init.d/redis_6379
Edit the init script.
sudo vi /etc/init.d/redis_6379
Make sure to modify REDIS_PORT accordingly to the port you are using. Both the pid file path and the configuration file name depend on the port number.
Copy the template configuration file you'll find in the root directory of the Redis distribution into /etc/redis/ using the port number as name, for instance:
sudo cp redis.conf /etc/redis/6379.conf