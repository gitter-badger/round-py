# patchboard.py
#
# Copyright 2014 BitVault.


import base64

import patchboard

from .client import Client


api_url = u"http://bitvault.pandastrike.com/"


__patchboard_client = None


def client(url=api_url):
    global __patchboard_client

    if __patchboard_client is None:
        __patchboard_client = patchboard.discover(url,
                                                  {u'default_context': Context})
    return Client(__patchboard_client.spawn())


def authed_client(url=api_url,
                  email=None,
                  password=None,
                  app_url=None,
                  api_token=None):
    cl = client(url)
    if email and password:
        cl.context.set_basic(email, password)
    elif app_url and api_token:
        cl.context.set_token(api_token)
    else:
        raise ValueError(
            u"Must supply either email and password, or url and token")
    return cl


class Context(dict):

    def authorizer(self, scheme, resource, action):
        if scheme == u"Basic":
            if hasattr(self, u'basic'):
                return self.basic
            else:
                raise Exception(u"Must call set_basic(email, password) first")

        elif scheme == u"BitVault-Token":
            if hasattr(self, u'api_token'):
                return self.api_token
            else:
                raise Exception(u"Must call set_token(api_token) first")

    def set_basic(self, email, password):
        string = u':'.join([email, password])
        self.basic = base64.b64encode(string)

    def set_token(self, token):
        self.api_token = token
