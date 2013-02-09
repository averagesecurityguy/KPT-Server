KnownPlainText Build Instructions

# Redis Server
A proper install using an init script is strongly suggested. The following instructions can be used to perform a proper installation using the init script shipped with Redis 2.4 in a Debian or Ubuntu based distribution.
We assume you already copied redis-server and redis-cli executables under /usr/local/bin.
Create a directory where to store your Redis config files and your data:
sudo mkdir /etc/redis sudo mkdir /var/redis
Copy the init script that you'll find in the Redis distribution under the utils directory into /etc/init.d. We suggest calling it with the name of the port where you are running this instance of Redis. For example:
sudo cp utils/redisinitscript /etc/init.d/redis_6379
Edit the init script.
sudo vi /etc/init.d/redis_6379
Make sure to modify REDIS_PORT accordingly to the port you are using. Both the pid file path and the configuration file name depend on the port number.
Copy the template configuration file you'll find in the root directory of the Redis distribution into /etc/redis/ using the port number as name, for instance:
sudo cp redis.conf /etc/redis/6379.conf
Create a directory inside /var/redis that will work as data and working directory for this Redis instance:
sudo mkdir /var/redis/6379
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
