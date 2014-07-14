#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '0.1.0'
__description__ = 'A command-line tool using Evernote as a pastebin service'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from argparse import ArgumentParser
from config import get_token
from evernote.api.client import EvernoteClient
from evernote.edam.type.ttypes import Note, NoteSortOrder
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import re


class EPaste(object):
    def __init__(self):
        self.tk = get_token()
        self.cl = EvernoteClient(token=self.tk, sandbox=True)
        self.ns = self.cl.get_note_store()

    def get(self, fp):
        guid = self.search(fp)
        if guid:
            note = ENote(self.ns.getNoteContent(self.tk, guid))
            note.title = fp
            note.guid = guid
            return note
        return False

    def put(self, enote):
        note = Note()
        note.title = enote.title
        note.content = enote.enml
        # note.notebookGuid = enote.bguid
        return self.ns.createNote(note)

    def search(self, fp):
        fl = NoteFilter(order=NoteSortOrder.UPDATED)
        fl.words = 'intitle:"%s"' % fp
        sp = NotesMetadataResultSpec(includeTitle=True)
        result = self.ns.findNotesMetadata(self.tk, fl, 0, 1, sp).notes
        if result:
            return result[0].guid
        return False

    def delete(self, fp, guid=None):
        if not guid:
            guid = self.search(fp)
        if guid:
            self.ns.deleteNote(self.tk, guid)


class ENote(object):
    def __init__(self, content):
        self.enml = content
        self.title = 'ENPaste'
        self.bguid = ''

    def __str__(self):
        return self.enml

    @staticmethod
    def enml2text(enml):
        text = re.sub(r'\r', '', enml)
        text = re.sub(r'<div><br/></div>', '', text)
        text = re.sub(r'</div>', '\n', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&amp;', '&')
        text = text.replace('&apos;', "'")
        text = text.replace('&gt;', '>')
        text = text.replace('&lt;', '<')
        text = text.replace('&quot;', '"')
        return text.strip()

    @staticmethod
    def text2enml(text):
        text = text.replace('&', '&amp;')
        text = text.replace("'", '&apos;')
        text = text.replace('>', '&gt;')
        text = text.replace('<', '&lt;')
        text = text.replace('"', '&quot;')
        return '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note><pre>%s</pre></en-note>''' % text

    def show(self):
        return ENote.enml2text(self.enml)

    def tofile(self):
        with open(self.title, 'w') as fw:
            fw.write(ENote.enml2text(self.enml))


def fromfile(fp):
    with open(fp) as fr:
        text = fr.read().strip()
    note = ENote(ENote.text2enml(text))
    note.title = fp
    return note


def main():
    parser = ArgumentParser(description=__description__, version=__version__)
    c = ['get', 'put']
    parser.add_argument('action', choices=c, help='the action to take')
    parser.add_argument('file')
    args = parser.parse_args()
    en = EPaste()
    if args.action == 'get':
        note = en.get(args.file)
        if note:
            print note.show()
        else:
            print 'No such file: "%s".' % args.file
    else:
        try:
            en.put(fromfile(args.file))
        except IOError:
            print 'No such file: "%s".' % args.file


if __name__ == '__main__':
    main()
