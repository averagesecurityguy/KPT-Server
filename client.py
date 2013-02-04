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


def parse_hash_file(name):
    passwords = []
    if os.path.exists(name) and os.path.isfile(name):
        data = open(name, 'r')

        for line in data:
            line = line.rstrip('\r\n')
            try:
                user, uid, lm, nt, comment, home, junk = line.split(':')
            except:
                error('Cannot parse hash file. Must be in pwdump format.')

            pwd = {'user': user, 'lm': lm, 'nt': nt}
            passwords.append(pwd)

    else:
        error('The hash file {0} does not exist or is not a file.'.format(name))

    return passwords


def process_passwords(resp):
    for p in resp:
        print '{0}:{1}'.format(p['user'], p['plain'])

    print 'Cracked {0} of {1} passwords.'.format(len(resp), len(passwords))


if __name__ == '__main__':
    creds = load_credentials('crackit.key')
    url = 'http://127.0.0.1:8080/'

    if len(sys.argv) != 2:
        error('Usage: crack_client hash_file')

    hash_file = sys.argv[1]
    passwords = parse_hash_file(hash_file)
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
