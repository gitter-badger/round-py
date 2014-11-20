# -*- coding: utf-8 -*-
# addresses.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from wrappers import ListWrapper

class Addresses(ListWrapper):

    def __init__(self, resource, client):
        self.collection_list = []
        super(Addresses, self).__init__(resource, client)

    def add(self, address):
        self.collection_list.append(address)

    def wrap(self, address):
        return address

    def create(self):
        address = self.resource.create()
        self.add(address)
        return address