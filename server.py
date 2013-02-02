#!/usr/bin/env python

import web
import json
import server_oauth
import time
import crack


web.config.debug = False
# Setup routing
urls = (
  '/', 'Index',
)


def error(msg):
    return '{{"Error":"{0}"}}'.format(msg)


def parse_auth_header(header):
    '''Parse the authorization header into a dictionary. If there are any
    problems parsing then return None, else return the dictionary.'''
    p = {}
    try:
        params = header.split(' ')
        params.pop(0)

        for h in params:
            k, v = h.split('=')
            p[k] = v.replace('"', '').replace(',', '')
    except:
        p = None
    finally:
        return p


def get_request_authorization():
    # Verify we have an authorization header. If not return error.
    ah = web.ctx.env.get('HTTP_AUTHORIZATION')
    ap = parse_auth_header(ah)

    return ah, ap


def get_url():
    return web.ctx.home + web.ctx.fullpath


class Index:
    def POST(self):
        # Process the authorization header.
        auth_header, auth_params = get_request_authorization()
        if (auth_header is None) or (auth_params is None):
            return error('Invalid authorization header.')

        # Find user and verify the user exists
        user = crack.lookup_user(auth_params['oauth_consumer_key'])
        if user is None:
            return error('Unauthorized request')

        # Verify authorization header
        auth = server_oauth.SimpleOAuth(user['auth']['consumer_key'],
                                        user['auth']['consumer_secret'],
                                        user['auth']['access_token'],
                                        user['auth']['access_token_secret'],
                                        get_url(),
                                        auth_params['oauth_timestamp'],
                                        auth_params['oauth_nonce'],
                                        web.data(),
                                        'POST')

        # Verify the user's authorization header
        if auth_header != auth.calculate_oauth():
            return error('Unauthorized request')

        # Verify user's subscription has not expired
        if int(time.time()) > user['expiration']:
            return error('Subscription Expired.')

        # Verify user has not exceeded maximum cracks
        if user['cracked_count'] > user['cracked_max']:
            return error('Exceeded licensed number of cracks.')

        update_crack_count(user['auth']['consumer_key'])
        request = json.loads(web.input()['input'])

        # Get cracked passwords
        return json.dumps(crack.crack_passwords(request))


def notfound():
    return error('Page Not Found')


app = web.application(urls, locals())
app.notfound = notfound

#application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
