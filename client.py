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


if __name__ == '__main__':
    creds = load_credentials('crackit.key')

    auth = oauth.TwitterSingleOauth(creds['consumer_key'],
                                    creds['consumer_secret'],
                                    creds['access_token'],
                                    creds['access_token_secret'])

    data = {'type': 'LM',
            'passwords': [{'hash': '1234567890'},
                          {'hash': '0987654321'}
                         ]
           }

    resp = requests.post('http://127.0.0.1:8080/', data=data)
    print resp.json()
