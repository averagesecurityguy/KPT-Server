import requests
import oauth
import os
import json
import sys
import base64


def error(msg):
    print msg
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


def parse_hash_file(hash_type, name):
    passwords = []
    if os.path.exists(name) and os.path.isfile(name):
        data = open(name, 'r')

        for line in data:
            user = None
            lm = None
            nt = None
            line = line.rstrip('\r\n')
            try:
                if hash_type == 'PWDUMP':
                    user, uid, lm, nt, comment, home, junk = line.split(':')
                elif hash_type == 'LM':
                    user, lm = line.split(':')
                else:
                    user, nt = line.split(':')

            except:
                error('Error: Cannot parse hash file')

            pwd = {'user': user, 'lm': lm, 'nt': nt}
            passwords.append(pwd)

    else:
        error('Error: {0} does not exist or is not a file.'.format(name))

    return passwords


def process_response(resp):
    for p in resp['passwords']:
        print '{0}:{1}:{2}'.format(p['user'], p['hash'], p['plain'])


if __name__ == '__main__':
    creds = load_credentials('crackit.key')

    if len(sys.argv) != 3:
        error('Usage: crack_client type hash_file')

    hash_type, hash_file = sys.argv[1:]
    hash_type = hash_type.upper()

    if hash_type not in ['LM', 'NTLM', 'PWDUMP']:
        error('Error: Invalid hash type, must use lm, ntlm, or pwdump')

    url = 'http://127.0.0.1:8080/'
    passwords = parse_hash_file(hash_type, hash_file)
    print passwords

    request = {'type': hash_type, 'passwords': passwords}
    data = {'input': json.dumps(request)}

    auth = oauth.SimpleOAuth(creds['consumer_key'].encode('ascii'),
                             creds['consumer_secret'].encode('ascii'),
                             creds['access_token'].encode('ascii'),
                             creds['access_token_secret'].encode('ascii')
                            )

    print 'Processing '
    resp = requests.post(url, data=data, auth=auth)
    process_response(resp.json())
