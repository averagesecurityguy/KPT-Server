#!/usr/bin/env python
import requests
import oauth
import os
import json
import sys
import base64


def error(msg):
    print 'Error: ' + msg
    sys.exit(1)


def load_credentials(filename):
    '''If the file exists and is a file then open it and attempt to load the
    credentials as a json string. If there are no errors return the loaded
    credentials.'''

    if not (os.path.exists(filename) and os.path.isfile(filename)):
        error('Key file {0} does not exist or is not a file.'.format(filename))

    try:
        data = base64.b64decode(open(filename).read())
        creds = json.loads(data)
    except:
        error('Could not load credentials from file {0}'.format(filename))

    if 'consumer_key' not in creds:
        error('Cannot find consumer_key in key file.')
    if 'consumer_secret' not in creds:
        error('Cannot find consumer_secret in key file.')
    if 'access_token' not in creds:
        error('Cannot find access_token in key file.')
    if 'access_token_secret' not in creds:
        error('Cannot find access_token_secret in key file.')

    return creds


def parse_hash_file(name, method):
    passwords = []
    if os.path.exists(name) and os.path.isfile(name):
        for line in open(name, 'r'):
            line = line.rstrip('\r\n')
            try:
                if method == '-p':
                    user, uid, lm, nt, comment, home, junk = line.split(':')
                elif method == '-f':
                    lm, nt = line.split(':')
                else:
                    error('Must specify a valid file type -p or -f')
            except:
                error('Hash file must be in pwdump or lm:nt format.')

            if method == '-p':
                # Skip machine acounts
                if user.endswith('$'):
                    continue
                users[user] = nt.upper()

            pwd = {'lm': lm, 'nt': nt}
            passwords.append(pwd)

    else:
        error('The hash file {0} does not exist or is not a file.'.format(name))

    return passwords


def process_passwords(resp):
    count = 0
    if users == []:
        for p in resp:
            count += 1
            print '{0}:{1}'.format(p, resp[p])

    else:
        for u in users:
            try:
                print '{0}:{1}'.format(u, resp[users[u]])
                count += 1
            except KeyError:
                pass

    print 'Cracked {0} of {1} passwords.'.format(count, len(passwords))


def usage():
    msg = 'Usage: client.py -p|-f hash_file'
    msg += '\nUse the -p option to designate the hash_file is in pwdump format.'
    msg += 'Use the -f option to designate the hash_file is in lm:ntlm format.'

    return msg


if __name__ == '__main__':
    pathname = os.path.dirname(sys.argv[0])       
    path = os.path.abspath(pathname)

    creds = load_credentials(os.path.join(path, 'license.key'))
    url = 'https://knownplaintext.co/crack'

    if len(sys.argv) != 3:
        print usage()
        sys.exit(1)

    if (sys.argv[1] != '-p') and (sys.argv[1] != '-f'):
        print usage()
        sys.exit(1)

    users = {}
    passwords = parse_hash_file(sys.argv[2], sys.argv[1])
    data = {'input': json.dumps(passwords)}

    auth = oauth.SimpleOAuth(creds['consumer_key'].encode('ascii'),
                             creds['consumer_secret'].encode('ascii'),
                             creds['access_token'].encode('ascii'),
                             creds['access_token_secret'].encode('ascii')
                            )

    print 'Sending hashes to server.'
    resp = requests.post(url, data=data, auth=auth)

    print 'Processing response.'
    if 'error' in resp.json():
        error(resp.json()['error'])
    else:
        process_passwords(resp.json())
