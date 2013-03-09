#!/usr/bin/env python

import web
import json
import time

import server_oauth
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
    '/crack', 'Crack',
    '/success', 'Success',
    '/cancel', 'Cancel',
    '/stats', 'Stats',
    '/downloads', 'Downloads',
    '/contact', 'Contact',
    '/buy', 'Buy'
)

# Configure the site template
render = web.template.render('/var/www/crack/templates/', base='layout')


class Index:
    def GET(self):
        return render.home()


class Success:
    def GET(self):
        return render.success()


class Cancel:
    def GET(self):
        return render.cancel()


class Stats:
    def GET(self):
        stats = crack_db.generate_stats()
        return render.stats(stats)


class Downloads:
    def GET(self):
        raise web.seeother('https://github.com/averagesecurityguy/KnownPlainText')
        #return render.downloads()


class Contact:
    def GET(self):
        return render.contact()


class Buy:
    def GET(self):
        return render.buy()


class Crack:
    def GET(self):
        raise web.seeother('/')

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
        if user['hash_count'] > user['hash_max']:
            return error('Exceeded licensed number of submissions.')

        # Extract hashes from web request and crack them
        request = json.loads(web.input()['input'])

        # Only crack as many passwords as there are hashes left.
        cracked = {}
        for hash in request:
            crack_db.update_hash_count(user['consumer_key'], 1)

            nt, plain = crack_db.crack_passwords(hash)
            if plain is not None:
                crack_db.update_crack_count(user['consumer_key'], 1)
                cracked[nt] = plain

        return json.dumps(cracked)


app = web.application(urls, locals())
app.notfound = notfound

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
