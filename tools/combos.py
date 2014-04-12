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
    posts = []
    pres = []

    pres = ['@', '!', '#', '$', '?', '*', '%', '=']
    pres = ['..', '!@', '**', '$$', '$4', '$0']
    pres = ['#1', '1_', '1@', '1=', '1!', '1%', '1$', '1*', '1-', '1.']
    pres = ['!1', '!2', '2@', '2-', '#2', '3-', '#3', '4$', '4_', '!4']
    pres = ['12@', '12#', '99.', '$$$', '!!!']
    pres = ['123', '12345', '123456']

    posts.extend(['!', '@', '#', '$', ';', ',', '.', '+', "'", '?', '*', '/'])
    posts.extend([',', '-', '&', ')'])
    posts.extend(['..', '++', '!!', '__', '&&', '1!', '#1', '1@', '@1', '!@'])
    posts.extend(['&*', '??', ',.', '?!', '.,', '..', '#$', '!#', '**', '*!'])
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
        posts.append('0' + str(i))
        posts.append(' ' + str(i))
        posts.append('.' + str(i))
        posts.append('$' + str(i))
        posts.append('@' + str(i))
        posts.append('-' + str(i))
        posts.append('#' + str(i))
        posts.append(',' + str(i))
        posts.append('+' + str(i))
        posts.append('_' + str(i))
        posts.append('&' + str(i))
        posts.append('!' + str(i))
        posts.append('*' + str(i))
        posts.append('@0' + str(i))
        posts.append('#0' + str(i))
        posts.append('_0' + str(i))
        posts.append(' 0' + str(i))
        posts.append('-0' + str(i))
        posts.append('*0' + str(i))




        pres.append(str(i))
        pres.append('0' + str(i))

    for i in xrange(10, 104):
        posts.append(str(i))
        posts.append('@' + str(i))
        posts.append('#' + str(i))

    for i in xrange(1963, 2016):
        posts.append(str(i))

    tmp = []

    tmp.append(word)
    tmp.append(word + word)
    for p in posts:
        tmp.append(word + p)

    for p in pres:
        tmp.append(p + word)

    return tmp


#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------

if len(sys.argv) != 2:
    print 'USAGE: combos.py file'
    sys.exit(1)

combos_from_file(sys.argv[1])
