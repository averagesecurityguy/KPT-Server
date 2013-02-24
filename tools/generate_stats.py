import redis
import json

user_db = redis.StrictRedis(host='localhost', port=6379, db=0)
lm_db = redis.StrictRedis(host='localhost', port=6379, db=1)
nt_db = redis.StrictRedis(host='localhost', port=6379, db=2)
stats_db = redis.StrictRedis(host='localhost', port=6379, db=4)

stats_db.set('lm_size', lm_db.dbsize())
stats_db.set('nt_size', nt_db.dbsize())

hcounts = user_db.keys('*:hash_count')
ccounts = user_db.keys('*:cracked_count')

hash_count = 0
for c in hcounts:
    hash_count += int(user_db.get(c))

stats_db.set('hash_count', hash_count)

cracked_count = 0
for c in ccounts:
    cracked_count += int(user_db.get(c))

stats_db.set('cracked_count', cracked_count)

if hash_count == 0:
    rate = 0.0
else:
    rate = float(cracked_count) / hash_count

stats_db.set('rate', int(100 * rate))

#nt_keys = nt_db.keys('*')

#hashes = []
#for hash in nt_keys:
#    data = json.loads(nt_db.get(hash))
#    if data['count'] > 0:
#        hashes.append((hash, data['count']))
#
#shashes = sorted(hashes, key=lambda t: t[2], reverse=True)
#print shashes[:100]
