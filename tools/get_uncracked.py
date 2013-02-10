import redis
import sys

if len(sys.argv) != 1:
    print 'USAGE: get_uncracked.py'
    sys.exit()

uc_db = redis.StrictRedis(host='localhost', port=6379, db=3)

count = 0
for k in uc_db.keys():
    user = 'User' + str(count)
    uid = count
    lm = uc_db.get(k)
    nt = k
    print '{0}:{1}:{2}:{3}:::'.format(user, uid, lm, nt)
