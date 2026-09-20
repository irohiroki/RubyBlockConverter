"""
Tests for the brace_to_do_end and do_end_to_brace commands.

Each pair of before-*.rb and after-*.rb in this directory makes one test
case. In a before file `@` marks a cursor: the markers are stripped before
the text goes into the buffer and their offsets become the selection. The
command then runs once with every cursor set, and the resulting buffer is
compared with the after file as a whole.

The commands call into the sublime API and delegate indentation to the
built-in reindent command, so these tests only run inside Sublime Text:
install UnitTesting (https://github.com/SublimeText/UnitTesting) and run
"UnitTesting: Test Current Package" from the command palette.
"""

import os

import sublime
from unittesting import DeferrableTestCase

CURSOR = '@'
FIXTURE_DIR = os.path.dirname(os.path.abspath(__file__))
RUBY_SYNTAX = 'Packages/Ruby/Ruby.sublime-syntax'
SYNTAX_LOAD_WAIT = 200


def read_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name)) as f:
        return f.read()


def strip_cursors(text):
    chunks = text.split(CURSOR)
    points = []
    offset = 0
    for chunk in chunks[:-1]:
        offset += len(chunk)
        points.append(offset)
    return ''.join(chunks), points


class ConvertBlockTestCase(DeferrableTestCase):
    def setUp(self):
        self.maxDiff = None
        self.view = sublime.active_window().new_file()
        self.view.set_scratch(True)
        self.view.set_syntax_file(RUBY_SYNTAX)
        settings = self.view.settings()
        settings.set('tab_size', 2)
        settings.set('translate_tabs_to_spaces', True)

    def tearDown(self):
        self.view.window().focus_view(self.view)
        self.view.window().run_command('close_file')

    def fill(self, fixture):
        text, points = strip_cursors(read_fixture(fixture))
        self.view.run_command('append', {'characters': text})
        sel = self.view.sel()
        sel.clear()
        for point in points:
            sel.add(sublime.Region(point))

    def contents(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def convert(self, command, before, after):
        self.fill(before)
        yield SYNTAX_LOAD_WAIT
        self.view.run_command(command)
        self.assertEqual(self.contents(), read_fixture(after))

    def test_brace_to_do_end(self):
        for step in self.convert(
                'brace_to_do_end',
                'before-BraceToDoEnd.rb', 'after-BraceToDoEnd.rb'):
            yield step

    def test_do_end_to_brace(self):
        for step in self.convert(
                'do_end_to_brace',
                'before-DoEndToBrace.rb', 'after-DoEndToBrace.rb'):
            yield step
