import sys
import redis
import sqlite3
import smbpasswd
import json


#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def usage():
    print 'USAGE: add_hashes.py [lm|ntlm] file'


def combos(word):
    posts = []
    pres = []

    pres = ['1', '2', '#1', '12345', '123456']

    posts.extend(['!', '@', '#', '$', ';', ',', '.', '..', "'"])
    posts.extend(['?', '!!', '*', '1!', '#1', '1@', '@1', '!@'])
    posts.extend(['555', '247', '174', '808', '160', '420', '423', '222'])
    posts.extend(['221', '522', '234', '143', '999', '121', '629', '200'])
    posts.extend(['202', '224', '929', '789', '159', '213', '210', '911'])
    posts.extend(['504', '199', '198', '900', '619', '611', '617', '182'])
    posts.extend(['187', '777', '666', '318', '313', '316', '001', '000'])
    posts.extend(['007', '305', '010', '711', '444', '333', '131', '456'])
    posts.extend(['323', '321', '122', '123', '125', '127', '111', '112'])
    posts.extend(['720', '6969', '1122', '1123', '1234', '0312', '8888'])
    posts.extend(['1212', '1214', '2121', '12345', '123456', '123123'])
    posts.extend(['4321', '2112', '!@#', '123!@#'])

    for i in xrange(0, 10):
        posts.append(str(i))
        posts.append("0" + str(i))

    for i in xrange(10, 104):
        posts.append(str(i))

    for i in xrange(1969, 2016):
        posts.append(str(i))

    tmp = []

    tmp.append(word)
    tmp.append(word + word)
    for p in posts:
        tmp.append(word + p)

    for p in pres:
        tmp.append(p + word)

    return tmp


def add_lm_hashes(pwds):
    for p in pwds:
        if len(p) > 14:
            continue
        val = "'{0}','{1}'".format(smbpasswd.lmhash(p).upper(), p)
        c.execute("INSERT INTO lm VALUES(" + val + ")")
        lm_db.commit()


def add_ntlm_hashes(pwds):
    for p in pwds:
        nt = {'plain': p, 'count': 0}
        nt_db.set(smbpasswd.nthash(p).upper(), json.dumps(nt))


#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------

if len(sys.argv) != 2:
    usage()
    sys.exit(1)

if (sys.argv[1] != 'lm') or (sys.argv[1] != 'ntlm'):
    usage()
    sys.exit(1)
else:
    type = sys.argv[1]

# Configure databases
nt_db = redis.StrictRedis(host='localhost', port=6379, db=2)
lm_db = sqlite3.connect('/var/redis/6379/lm.db')
c = lm_db.cursor()

# Create the LM hash table if it does not exist.
c.execute("CREATE TABLE IF NOT EXISTS lm (hash text, plain text)")

try:
    f = open(sys.argv[2], 'r')
except:
    print 'Could not open file: {0}'.format(f.name())

for line in f:
    line = line.rstrip()

    if type == 'lm':
        add_lm_hashes(combos(line.upper()))

    if type == 'ntlm':
        add_ntlm_hashes(combos(line))
        add_ntlm_hashes(combos(line.capitalize()))
