import redis
import hashlib
import binascii
import itertools
import re
import json

hash_re = re.compile(r'[0-9A-Fa-f]{32}')

user_db = redis.StrictRedis(host='localhost', port=6379, db=0)
lm_db = redis.StrictRedis(host='localhost', port=6379, db=1)
nt_db = redis.StrictRedis(host='localhost', port=6379, db=2)
uc_db = redis.StrictRedis(host='localhost', port=6379, db=3)
stats_db = redis.StrictRedis(host='localhost', port=6379, db=4)


def generate_stats():
    stats = {}
    stats['lm_size'] = stats_db.get('lm_size')
    stats['nt_size'] = stats_db.get('nt_size')
    stats['hash_count'] = stats_db.get('hash_count')
    stats['cracked_count'] = stats_db.get('cracked_count')
    stats['rate'] = stats_db.get('rate')

    return stats


def convert_lm_to_ntlm(lm_plain, nt):
    combos = map(''.join, itertools.product(*((c.upper(),
                                               c.lower()) for c in lm_plain)))

    for c in combos:
        hash = hashlib.new('md4', c.encode('utf-16le')).digest()
        if binascii.hexlify(hash).upper() == nt:
            return c

    return None


def crack_passwords(hash):
    '''Lookup the hash in the database. If we find the nt hash then use it.
    If not, see if we have the lm hash and convert it to nt. If neither are
    there, then set plain to None.'''

    # Normalize our hashes.
    lm = hash['lm'].upper()
    nt = hash['nt'].upper()

    # Verify the data we were sent looks like a hash. If not, set them to
    # empty strings.
    m = hash_re.search(lm)
    if m is None:
        lm = ''

    m = hash_re.search(nt)
    if m is None:
        nt = ''

    # Process the hashes to find the plaintext. If the NTLM is in the
    # database, then use it. If it is not, then see if the LM hash is in
    # the database and convert it to NTLM to ensure we have the correct
    # case.
    data = nt_db.get(nt)

    if data is not None:
        crack = json.loads(data)
        crack['count'] += 1
        nt_db.set(nt, json.dumps(crack))
        return nt, crack['plain']
    else:
        data = lm_db.get(lm)
        if data is not None:
            crack = json.loads(data)
            crack['count'] += 1
            lm_db.set(lm, json.dumps(crack))

            plain = convert_lm_to_ntlm(crack['plain'], nt)
            if plain is not None:
                data = {'plain': plain, 'count': 1}
                nt_db.set(nt, json.dumps(data))
                return nt, plain
        else:
            uc_db.set(nt, lm)
            return None, None


def update_hash_count(ck, val):
    user_db.incr(ck + ':hash_count', val)


def update_hash_max(ck, val):
    user_db.incr(ck + ':hash_max', val)


def update_crack_count(ck, val):
    user_db.incr(ck + ':cracked_count', val)


def get_user(consumer_key):
    '''Lookup user in the database. If the user exists return the user record
    if not, then return None.'''

    user = {}

    user['consumer_key'] = user_db.get(consumer_key + ":consumer_key")
    if user['consumer_key'] is not None:
        user['consumer_secret'] = user_db.get(consumer_key + ":consumer_secret")
        user['access_token'] = user_db.get(consumer_key + ":access_token")
        user['access_token_secret'] = user_db.get(consumer_key + ":access_token_secret")
        user['expiration'] = user_db.get(consumer_key + ":expiration")
        user['hash_count'] = int(user_db.get(consumer_key + ":hash_count"))
        user['hash_max'] = int(user_db.get(consumer_key + ":hash_max"))
    else:
        user = None

    return user
