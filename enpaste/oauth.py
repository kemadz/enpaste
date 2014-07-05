#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import Conf
from evernote.api.client import EvernoteClient
from getpass import getpass
import os
import requests
import sys


def get_access_token_via_oauth(conf=Conf):
    CONF_PATH = os.path.join(os.getenv('HOME'), '.enpaste')
    try:
        with open(CONF_PATH) as fr:
            token = fr.read().strip()
        if token:
            return token
    except:
        pass

    client = EvernoteClient(
        consumer_key=conf.key,
        consumer_secret=conf.sec,
        sandbox=conf.env
    )
    token = client.get_request_token(conf.url)
    url = client.get_authorize_url(token)
    c = requests.session()
    resp = c.get(url)

    print '==> Please Sign in.'
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
    token = client.get_access_token(
        token['oauth_token'],
        token['oauth_token_secret'],
        resp.headers['location'].split('?')[1].split('&')[1].split('=')[1]
    )
    with open(CONF_PATH, 'w') as fw:
        fw.write(token)
    return token


def main():
    get_access_token_via_oauth()


if __name__ == '__main__':
    main()
