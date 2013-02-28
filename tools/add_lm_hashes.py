import redis
import smbpasswd
import sys
import json

if len(sys.argv) != 2:
    print 'USAGE: add_lm_hashes.py file'
    sys.exit()

lm_db = redis.StrictRedis(host='localhost', port=6379, db=1)


def add_lm_hash(hash, plain):
    # print 'Adding LM hash {0}'.format(hash)
    lm = {'plain': plain, 'count': 0}
    lm_db.set(hash.upper(), json.dumps(lm))


for line in open(sys.argv[1]):
    line = line.rstrip('\r\n')
    print 'Adding ' + line

    # LM truncates at 14 characters.
    if len(line) <= 14:
        add_lm_hash(smbpasswd.lmhash(line), line)
