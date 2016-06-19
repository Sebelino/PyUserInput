#!/usr/bin/env python

from threading import Thread
from pykeyboard import PyKeyboard
from pykeyboard import PyKeyboardEvent


def test_keylistener_init():
    PyKeyboardEvent()


class TestKeyPressAndRelease:
    def undokeytap(cls, n):
        """ Erase crap written to stdout during tests. """
        cls.kb.tap_key('BackSpace', n=n)

    @classmethod
    def setup_class(cls):
        cls.kb = PyKeyboard()

    def setup(self):
        self.kl = PyKeyboardEvent()
        Thread(target=self.kl.run).start()

    def press_and_release_keysequence(self, keys):
        currentlypressed = set()
        try:
            for key in keys:
                self.kb.press_key(key)
                currentlypressed.add(key)
        finally:
            for key in currentlypressed:
                self.kb.release_key(key)

    def test_queue_put_x(self):
        self.expected = {
            'x': (1, {'x'}),
        }
        self.backspaces = 1
        self.press_and_release_keysequence(['x'])

    def test_queue_put_xyz(self):
        self.expected = {
            'x': (1, {'x'}),
            'y': (2, {'x', 'y'}),
            'z': (3, {'x', 'y', 'z'}),
        }
        self.backspaces = 3
        self.press_and_release_keysequence(['x', 'y', 'z'])

    def teardown(self):
        self.kl.stop()
        self.undokeytap(self.backspaces)
