import redis
import base64
import time
import random
import string
import json

user_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def del_user(email):
    print 'Deleting user account.'
    ck = user_db.get(email)

    if ck is None:
        print 'User account is not in database.'
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
yn = raw_input('Are you sure you want to remove {0} from the database? '.format(email))
yn = yn.upper()
if (yn == 'Y') or (yn == 'YE') or (yn == 'YES'): 
    del_user(email)
else:
    print 'Cancelling.'
