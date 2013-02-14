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


def generate_stats():
    stats = {}
    stats['lm_size'] = lm_db.size()
    stats['nt_size'] = nt_db.size()
    
    hcounts = user_db.keys('*:hash_count')
    ccounts = user_db.keys('*:crack_count')

    stats['hash_count'] = 0
    for c in hcounts:
        stats['hash_count'] += int(users_db.get(c))

    stats['cracked_count'] = 0
    for c in ccounts:
        stats['cracked_count'] += int(users_db.get(c))

    if stats['hash_count'] == 0:
        rate = 0.0
    else:
        rate = float(stats['cracked_count']) / stats['hash_count']

    stats['rate'] = int(100 * rate)

    return stats 

def convert_lm_to_ntlm(lm_plain, nt):
    combos = map(''.join, itertools.product(*((c.upper(),
                                               c.lower()) for c in lm_plain)))

    for c in combos:
        hash = hashlib.new('md4', c.encode('utf-16le')).digest()
        if binascii.hexlify(hash).upper() == nt:
            return c

    return None


def crack_passwords(request):
    '''Lookup the hash in the database. If we find the nt hash then use it.
    If not, see if we have the lm hash and convert it to nt. If neither are
    there, then set plain to None.'''

    cracked = {}
    for p in request:
        # Verify the data we were sent looks like a hash. If not, set them to
        # empty strings.
        m = hash_re.search(p['lm'].upper())
        if m is None:
            p['lm'] = ''

        m = hash_re.search(p['nt'].upper())
        if m is None:
            p['nt'] = ''

        # Process the hashes to find the plaintext. If the NTLM is in the
        # database, then use it. If it is not, then see if the LM hash is in
        # the database and convert it to NTML to ensure we have the correct
        # case.
        data = nt_db.get(p['nt'].upper())

        if data is not None:
            crack = json.loads(data)
            crack['count'] += 1
            cracked[p['nt'].upper()] = crack['plain']
            nt_db.set(p['nt'], json.dumps(crack))
        else:
            data = lm_db.get(p['lm'].upper())
            if data is not None:
                crack = json.loads(data)
                crack['count'] += 1
                lm_db.set(p['lm'], json.dumps(crack))

                plain = convert_lm_to_ntlm(crack['plain'], p['nt'].upper())
                if plain is not None:
                    nt = {'plain': plain, 'count': 1}
                    nt_db.set(p['nt'].upper(), json.dumps(nt))
                    cracked[p['nt'].upper()] = plain
            else:
                uc_db.set(p['nt'].upper(), p['lm'].upper())

    return cracked


def update_hash_count(ck, val):
    user_db.incr(ck + ':hash_count', val)


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
    else:
        user = None

    return user
