#!/usr/bin/python
# -*- coding: utf-8 -*-

from evernote.api.client import EvernoteClient
import requests


def main():
    callback = 'https://www.evernote.com/'
    client = EvernoteClient(
        consumer_key='kemadz',
        consumer_secret='5e0516c3e4a06df0',
        # sandbox=False
    )
    request_token = client.get_request_token(callback)
    url = client.get_authorize_url(request_token)

    c = requests.session()
    resp = c.get(url)

    payload = {'login': 'Sign in', 'targetUrl': url}
    username = 'kemad@qq.com'
    password = '71f32998'
    payload['username'] = username
    payload['password'] = password

    resp = c.post(url, data=payload)

    payload = {'authorize': 'Authorize', 'embed': 'false'}
    payload['oauth_token'] = request_token['oauth_token']
    payload['oauth_callback'] = callback

    resp = c.post(url, data=payload, allow_redirects=False)

    access_token = client.get_access_token(
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        resp.headers['location'].split('?')[1].split('&')[1].split('=')[1]
    )

    print access_token


if __name__ == '__main__':
    main()
