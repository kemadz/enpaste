#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enpaste.config as ec
import os

ec.conf = ec.TestConfig()


def test_config_with_no_pth():
    try:
        os.unlink(ec.conf.pth)
    except:
        pass
    assert ec.get_token().startswith('S')


def test_config_with_pth():
    try:
        with open(ec.conf.pth) as fr:
            token = fr.read().strip()
    except:
        token = None
    assert token == ec.get_token()
