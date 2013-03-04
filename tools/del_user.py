import redis
import base64
import time
import random
import string
import json

user_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def del_user(email):
    print 'Creating new user account.'
    ck = user_db.get(email)

    user_db.delete(ck + ':email')
    user_db.delete(ck + ':consumer_key')
    user_db.delete(ck + ':consumer_secret')
    user_db.delete(ck + ':access_token')
    user_db.delete(ck + ':access_token_secret')
    user_db.delete(ck + ':expiration')
    user_db.delete(ck + ':cracked_count')
    user_db.delete(ck + ':hash_max') 
    user_db.delete(ck + ':hash_count')
    user_db.delete(email)

    print 'Deleted user {0}'.format(email)


# MAIN #
print 'Remove a user account from the database.'
email = raw_input('Enter the email address of the user to remove: ') 
del_user(email)
