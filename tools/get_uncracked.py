import redis
import sys

if len(sys.argv) != 1:
    print 'USAGE: get_uncracked.py'
    sys.exit()

uc_db = redis.StrictRedis(host='localhost', port=6379, db=3)
outfile = open('uncracked.pwdump', 'w')

count = 0
for k in uc_db.keys():
    user = 'User' + str(count)
    uid = count
    lm = uc_db.get(k)
    nt = k
    outfile.write('{0}:{1}:{2}:{3}:::\n'.format(user, uid, lm, nt))
    count += 1

outfile.flush()
outfile.close()

uc_db.flushdb()
