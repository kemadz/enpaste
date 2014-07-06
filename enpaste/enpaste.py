#!/usr/bin/python
# -*- coding: utf-8 -*-

from evernote.api.client import EvernoteClient


class enpaste(object):
    def __ini__(self, t):
        self.c = EvernoteClient(token=t)


def main():
    pass


if __name__ == '__main__':
    main()
