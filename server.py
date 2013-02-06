#!/usr/bin/env python

import web
import json
import server_oauth
import time
import crack_db


def error(msg):
    return '{{"error":"{0}"}}'.format(msg)


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


def notfound():
    return web.notfound(render.notfound())


web.config.debug = False
# Setup routing
urls = (
  '/', 'Index',
  '/crack', 'Crack'
)

# Configure the site template
render = web.template.render('templates/', base='layout')


class Index:
    def GET(self):
        return render.home()


class Crack:
    def GET(self):
        return web.notfound(render.notfound())

    def POST(self):
        # Process the authorization header.
        auth_header, auth_params = get_request_authorization()
        if (auth_header is None) or (auth_params is None):
            return error('Invalid authorization header.')

        # Find user and verify the user exists
        user = crack_db.get_user(auth_params['oauth_consumer_key'])
        if user is None:
            return error('Unauthorized request')

        # Verify authorization header
        auth = server_oauth.SimpleOAuth(user['consumer_key'],
                                        user['consumer_secret'],
                                        user['access_token'],
                                        user['access_token_secret'],
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
        # if user['cracked_count'] > user['cracked_max']:
        #     return error('Exceeded licensed number of cracks.')

        # Extract hashes from web request and crack them
        request = json.loads(web.input()['input'])
        cracked = crack_db.crack_passwords(request)

        # Update statistics
        crack_db.update_hash_count(user['consumer_key'], len(request))
        crack_db.update_crack_count(user['consumer_key'], len(cracked))

        return json.dumps(cracked)


app = web.application(urls, locals())
app.notfound = notfound

#application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
