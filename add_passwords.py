import redis
import smbpasswd

lm_db = redis.StrictRedis(host='localhost', port=6379, db=1)
nt_db = redis.StrictRedis(host='localhost', port=6379, db=2)


def add_lm_hash(hash, plain):
    print 'Adding LM hash {0}'.format(hash)
    lm_db.set(hash, plain)
    print lm_db.get(hash)
    lm_db.set(hash + ':count', 0)
    print lm_db.get(hash + ':count')


def add_nt_hash(hash, plain):
    print 'Adding NT hash {0}'.format(hash)
    nt_db.set(hash, plain)
    print nt_db.get(hash)
    nt_db.set(hash + ':count', 0)
    print nt_db.get(hash + ':count')

for line in open('passwords.txt'):
    line = line.rstrip('\r\n')
    print line
    add_lm_hash(smbpasswd.lmhash(line), line)
    add_nt_hash(smbpasswd.nthash(line), line)

