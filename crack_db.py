import redis
import hashlib
import binascii
import itertools
import re

hash_re = re.compile(r'[0-9A-Fa-f]{32}')

user_db = redis.StrictRedis(host='localhost', port=6379, db=0)
lm_db = redis.StrictRedis(host='localhost', port=6379, db=1)
nt_db = redis.StrictRedis(host='localhost', port=6379, db=2)
ucnt_db = redis.StrictRedis(host='localhost', port=6379, db=3)
uclm_db = redis.StrictRedis(host='localhost', port=6379, db=4)


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

    cracked = []
    for p in request:
        # Verify the data we were sent looks like a hash. If not, set them to
        # empty strings.
        m = hash_re(p['lm'].upper())
        if m is None:
            p['lm'] = ''

        m = hash_re(p['nt'].upper())
        if m is None:
            p['nt'] = ''

        # Process the hashes to find the plaintext. If the NTLM has is in the
        # database, then use it. If it is not, then see if the LM hash is in
        # the database and convert it to NTML to ensure we have the correct
        # case.
        lm_plain = lm_db.get(p['lm'].upper())
        nt_plain = nt_db.get(p['nt'].upper())

        if nt_plain is not None:
            update_nt_count(p['nt'].upper(), 1)
            cracked.append({p['nt'].upper(): nt_plain})
        else:
            if lm_plain is not None:
                update_lm_count(p['lm'].upper(), 1)
                nt_plain = convert_lm_to_ntlm(lm_plain, p['nt'].upper())
                if nt_plain is not None:
                    nt_db.set(p['nt'].upper(), nt_plain)
                    cracked.append({p['nt'].upper(): nt_plain})
            else:
                ucnt_db.set(p['nt'].upper(), '')
                uclm_db.set(p['lm'].upper(), '')

    return cracked


def update_lm_count(lm, val):
    count = lm_db.get(lm + ':count')
    lm_db.set(lm + ':count', int(count) + val)


def update_nt_count(nt, val):
    count = nt_db.get(nt + ':count')
    nt_db.set(nt + ':count', int(count) + val)


def update_hash_count(ck, val):
    count = user_db.get(ck + ':hash_count')
    user_db.set(ck + ':hash_count', int(count) + val)


def update_crack_count(ck, val):
    count = user_db.get(ck + ':cracked_count')
    user_db.set(ck + ':cracked_count', int(count) + val)


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
