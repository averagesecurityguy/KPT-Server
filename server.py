#!/usr/bin/env python

import web
import json
import time
import stripe
import re

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


def valid_email(address):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", address):
        return False
    else:
        return True


def notfound():
    return web.notfound(render.notfound())


web.config.debug = False
# Setup routing
urls = (
    '/', 'Index',
    '/crack', 'Crack',
    '/success', 'Success',
    '/tos', 'Tos',
    '/stats', 'Stats',
    '/downloads', 'Downloads',
    '/contact', 'Contact',
    '/buy', 'Buy'
)

# Configure the site template
# render = web.template.render('/var/www/crack/templates/', base='layout')
render = web.template.render('templates', base='layout')


class Index:
    def GET(self):
        return render.home(None)

    def POST(self):
        hash = {}
        try:
            lm, ntlm = web.input()['hash'].split(':')
            hash['lm'] = lm
            hash['nt'] = ntlm
        except:
            return render.home('Invalid Hash')

        nt, plain = crack_db.crack_passwords(hash)

        if plain is not None:
            return render.home(plain)
        else:
            return render.home('Not Found')


class Success:
    def GET(self):
        return render.success()


class Tos:
    def GET(self):
        return render.tos()


class Stats:
    def GET(self):
        stats = crack_db.generate_stats()
        return render.stats(stats)


class Downloads:
    def GET(self):
        raise web.seeother('https://github.com/averagesecurityguy/KnownPlainText')


class Contact:
    def GET(self):
        return render.contact()


class Buy:
    def GET(self):
        return render.buy(None)

    def POST(self):
        amt = 0
        email = web.input()['email']
        name = web.input()['name']
        ltype = web.input()['license']
        token = web.input()['stripeToken']

        # Validate Input
        errors = []
        if email == '':
            errors.append('Email cannot be empty')

        if valid_email(email) is not True:
            errors.append('You must enter a valid email address')

        if name == '':
            errors.append('Name can not be empty')

        if 'tos' not in web.input():
            errors.append('You must agree to the Terms Of Service')

        if errors != []:
            return render.buy(','.join(errors))

        # Set the payment amount
        if ltype == '7 Day License ($75)':
            amt = 7500

        if ltype == '30 Day License ($200)':
            amt = 20000

        if ltype == '1 Year License ($1000)':
            amt = 100000

        stripe.api_key = "sk_test_MC6LVX3YnsKv1vm3g0ZPBZSp"
        desc = '{0} - {1} - {2}'.format(name, email, ltype)
        try:
            stripe.Charge.create(
                amount=amt,
                currency="usd",
                card=token,
                description=desc
            )
        except stripe.CardError, e:
            return render.buy(e)

        except stripe.InvalidRequestError, e:
            return render.buy(e)

        return render.success()


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

#application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
