import redis
import base64
import time
import random
import string
import json

user_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def generate_random_string(l):
    key_space = string.ascii_lowercase + string.ascii_uppercase
    key_space += '0123456789'

    return "".join([random.choice(key_space) for x in xrange(l)])


def add_new_user(email):
    print 'Creating new user account.'
    ck = generate_random_string(16)
    cs = generate_random_string(32)
    at = generate_random_string(16)
    ats = generate_random_string(32)

    user_db.set(email, ck)
    user_db.set(ck + ':email', email)
    user_db.set(ck + ':consumer_key', ck)
    user_db.set(ck + ':consumer_secret', cs)
    user_db.set(ck + ':access_token', at)
    user_db.set(ck + ':access_token_secret', ats)
    user_db.set(ck + ':expiration', int(time.time()) + 365 * 24 * 60 * 60)
    user_db.set(ck + ':cracked_count', 0)
    user_db.set(ck + ':hash_count', 0)

    generate_license_key(ck, cs, at, ats)
    print 'Created new user {0}'.format(ck)


def generate_license_key(ck, cs, at, ats):
    key = {'consumer_key': ck,
           'consumer_secret': cs,
           'access_token': at,
           'access_token_secret': ats}

    print 'Saving license key to {0}.'.format(ck + '.key')
    key_file = open(ck + '.key', 'w')
    key_file.write(base64.b64encode(json.dumps(key)))
    key_file.close()


# MAIN #
print 'Add a new user account to the database.'
email = raw_input('Enter the email address of the user: ')
add_new_user(email)