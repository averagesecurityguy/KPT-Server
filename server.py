#!/usr/bin/env python

import web
import json
import server_oauth
import time

web.config.debug = False
# Setup routing
urls = (
  '/', 'Index',
)


def lookup_user(ck):
    user = {'auth': {'consumer_key': '123456789',
                     'consumer_secret': 'secret',
                     'access_token': '123456789',
                     'access_token_secret': 'secret'},
            'expiration': int(time.time()),
            'cracked_count': 0,
            'cracked_max': 1}

    return user


def update_crack_count(ck):
    pass


def crack_passwords(passwords):
    return {'type': 'LM',
            'passwords': [{'hash': '0123456789', 'plain': 'abcdefghij'},
                          {'hash': '9876543210', 'plain': 'jihgfedcba'}]
           }


class Index:
    def GET(self):
        # Parse request
        auth_header = ''
        ck = ''
        url = ''
        body = ''
        passwords = json.loads(body)

        # Verify Oauth
        user = lookup_user(ck)

        # Verify user exists
        if user == None:
            return {'Error': 'Unauthorized request'}

        ck = user['auth']['consumer_key']
        cs = user['auth']['consumer_secret']
        at = user['auth']['access_token']
        ats = user['auth']['access_token_secret']
        auth = server_oauth.SimpleOauth(ck, cs, at, ats, url, body, 'GET')

        # Verify the user's authorization header
        if auth_header != auth.calculate():
            return {'Error': 'Unauthorized request'}

        # Verify user's subscription has not expired
        if int(time.time()) > user['expiration']:
            return {'Error': 'Subscription Expired.'}

        # Verify user has not exceeded maximum cracks
        if user['cracked_count'] > user['cracked_max']:
            return {'Error': 'Exceeded licensed number of cracks.'}

        update_crack_count(ck)

        # Get cracked passwords
        return json.dumps(crack_passwords(passwords))


def notfound():
    return {'Error': 'Page Not Found'}


app = web.application(urls, locals())
app.notfound = notfound

#application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
