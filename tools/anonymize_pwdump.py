import sys

if len(sys.argv) != 2:
    print 'Usage: anonymize_pwdump.py file'
    sys.exit(1)


count = 0
for line in open(sys.argv[1], 'r'):
    line = line.rstrip()

    count += 1
    user, id, lm, nt, junk1, junk2, junk3 = line.split(':')

    user = 'User' + str(count)
    id = count

    print user + ':' + str(id) + ':' + lm + ':' + nt + ':::'
