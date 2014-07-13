#!/usr/bin/python
# -*- coding: utf-8 -*-

from evernote.api.client import EvernoteClient
from getpass import getpass
import os
import requests
import sys


class DefConfig(object):
    key = 'kemadz-0933'
    sec = 'b7ff6a209cb13596'
    url = 'https://www.evernote.com/'
    env = True  # False for debug
    pth = os.path.join(os.getenv('HOME'), '.enpaste')


class TestConfig(DefConfig):
    key = 'kemadz-2947'
    sec = '78caff530ac10b21'
    url = 'https://sandbox.evernote.com/'
    env = True
    username = 'test@qq.com'
    password = '71f32998'


conf = DefConfig()


def load_token():
    try:
        with open(conf.pth) as fr:
            token = fr.read().strip()
        if token:
            return token
    except:
        return False


def save_token(token):
    try:
        with open(conf.pth, 'w') as fw:
            fw.write(token)
    except:
        return False


def oauth():
    client = EvernoteClient(
        consumer_key=conf.key,
        consumer_secret=conf.sec,
        sandbox=conf.env
    )
    token = client.get_request_token(conf.url)
    url = client.get_authorize_url(token)
    c = requests.session()
    c.get(url)

    print '==> Please Sign in. Never store your PASSWORD!'
    cnt = 3
    while cnt:
        cnt -= 1
        payload = {'login': 'Sign in', 'targetUrl': url}
        if hasattr(conf, 'username'):
            payload['username'] = conf.username
        else:
            payload['username'] = raw_input('Username: ').strip()
        if hasattr(conf, 'password'):
            payload['password'] = conf.password
        else:
            payload['password'] = getpass().strip()
        resp = c.post(url, data=payload)
        if resp.history:
            break
        else:
            if not cnt:
                print 'Incorrect Username or Passowrd!'
                sys.exit(1)
            else:
                print 'Sorry, incorrect Username or Password.'
    print '<== Signed in.'

    payload = {'authorize': 'Authorize', 'embed': 'false'}
    payload['oauth_token'] = token['oauth_token']
    payload['oauth_callback'] = conf.url
    resp = c.post(url, data=payload, allow_redirects=False)
    return client.get_access_token(
        token['oauth_token'],
        token['oauth_token_secret'],
        resp.headers['location'].split('?')[1].split('&')[1].split('=')[1]
    )


def get_token():
    token = load_token()
    if not token:
        token = oauth()
        save_token(token)
    return token


def main():
    return get_token()


if __name__ == '__main__':
    main()
