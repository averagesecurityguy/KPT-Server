import redis
import smbpasswd
import sys
import json

if len(sys.argv) != 2:
    print 'USAGE: add_passwords.py file'
    sys.exit()

lm_db = redis.StrictRedis(host='localhost', port=6379, db=1)
nt_db = redis.StrictRedis(host='localhost', port=6379, db=2)


def add_lm_hash(hash, plain):
    # print 'Adding LM hash {0}'.format(hash)
    lm = {'plain': plain, 'count': 0}
    lm_db.set(hash.upper(), json.dumps(lm))


def add_nt_hash(hash, plain):
    # print 'Adding NT hash {0}'.format(hash)
    nt = {'plain': plain, 'count': 0}
    nt_db.set(hash.upper(), json.dumps(nt))

for line in open(sys.argv[1]
):
    line = line.rstrip('\r\n')
    print 'Adding ' + line

    # LM truncates at 14 characters.
    if len(line) <= 14:
        add_lm_hash(smbpasswd.lmhash(line), line)
    add_nt_hash(smbpasswd.nthash(line), line)
