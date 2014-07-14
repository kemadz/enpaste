#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enpaste


with open('tests/sample.enml') as fr:
    enml_sample = fr.read()

with open('tests/sample.text') as fr:
    text_sample = fr.read()

with open('tests/output.enml') as fr:
    enml_output = fr.read()

with open('tests/output.text') as fr:
    text_output = fr.read()

with open('setup.py') as fr:
    sample = fr.read().strip()


def test_text2enml():
    assert enpaste.ENote.text2enml(text_sample) == enml_output


def test_enml2text():
    assert enpaste.ENote.enml2text(enml_sample) == text_output


def test_enpaste_get_not_exist():
    assert not enpaste.EPaste().get('test_file_should_not_exist')


def test_enpaste_put_and_get():
    en = enpaste.EPaste()
    en.put(enpaste.fromfile('setup.py'))
    assert sample == en.get('setup.py').show()


def teardown():
    enpaste.EPaste().delete('setup.py')

test_enpaste_put_and_get.teardown = teardown
