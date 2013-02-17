import sys

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------

def combos_from_file(filename):

    try:
        f = open(filename, 'r')
    except:
        print "Could not open file: %s" % f.name()

    for line in f:
        line = line.rstrip()
        print '\n'.join(combos(line))
        print '\n'.join(combos(line.capitalize()))

	
def combos(word):
    adds = []

    adds.extend(['$', '123', '456', '789', '69', '6969', '89', '99', '1234'])
    adds.extend(['33', '44', '55', '66', '77', '88', '1977', '1978', '1979'])
    adds.extend(['1234', '4321', '007', '2112', '!', '@', '#', ])

    for i in xrange(0,10):
        adds.append(str(i))
        adds.append("0" + str(i))

    for i in xrange(10, 23):
        adds.append(str(i))

    for i in xrange(1990,2013):
        adds.append(str(i))

    tmp = []

    tmp.append(word)
    tmp.append(word + word)
    for a in adds:
        tmp.append(word + a)
        tmp.append(a + word)

    return tmp

    
#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------

if len(sys.argv) != 2:
    print 'USAGE: weak_passwords.py file'

words = [ "password", "welcome", "welc0me", "w3lcome", "w3lc0me", "changeme",
          "security"]

for w in words:
    print '\n'.join(combos(w))
    print '\n'.join(combos(w.capitalize()))

combos_from_file(sys.argv[1])
