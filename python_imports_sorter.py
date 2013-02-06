#!/usr/bin/python

""" Sublime plugin: python_imports_sorter
Author: marcin.kliks@gmail.com
License: MIT
Version 0.4
https://github.com/vi4m/sublime_python_imports
"""

import traceback

try:
    from organizer import Organizer
    # st2
except ImportError:
    # st3
    from .organizer import Organizer

from io import StringIO
from tokenize import INDENT, ERRORTOKEN, OP, NUMBER
from tokenize import generate_tokens
import tokenize

import sublime
import sublime_plugin


class SplitPythonArgumentsCommand(sublime_plugin.TextCommand):
    """Split long function arguments list into the new lines.
    E.g:

    func(5, x=1, y=2)

    to the form of:

    func(
        5,
        x=1,
        y=2
    )"""
    def run(self, edit):
        self.level = 0
        self.inside_call = 0
        self.previous = (0, 0)
        contents = self.view.substr(self.view.full_line(self.view.sel()[0]))
        full = ''
        for x in generate_tokens(StringIO(contents).readline):
            full += self.handle_token(x)

        self.view.replace(edit, r=self.view.full_line(self.view.sel()[0]), text=full)

    def handle_token(self, token):
        toknum, tokval, _, _, _ = token
        if self.previous[0] not in(
            0, INDENT
        ) and toknum not in(
            0, INDENT
        ) and not self.inside_call and tokval != '.' and self.previous[1] != '.' and str(
            tokval
        ) not in '[]():' and str(
            self.previous[1]
        ) not in '[(':
            spacing = ' '
        else:
            spacing = ''
        self.previous = (toknum, tokval)
        if toknum in(OP, ERRORTOKEN) and tokval == '(':
            self.inside_call +=1
            self.level +=1
            tokval = tokval + "\n" + self.level * '    '
        elif toknum in (OP, ERRORTOKEN) and tokval == ')':
            self.inside_call -=1
            self.level -=1
            tokval = "\n" + self.level * '    ' + tokval
        elif toknum in (OP, ERRORTOKEN) and tokval == ',':
            tokval = tokval + "\n" + self.level * '    '
        elif toknum == INDENT:
            self.level += len(tokval) // 4
            return tokval
        tokval = spacing + tokval
        return tokval


class SortImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            settings = sublime.load_settings("python_imports_sorter.sublime-settings")
            project_modules = ['sublime', 'sublime_plugin']
            additional_modules = settings.get('project_modules', [])
            if additional_modules:
                project_modules.extend(additional_modules)
            sublime.status_message('Formatting imports...')
            line_endings = self.view.line_endings()
            if line_endings == 'windows':
                delimiter = '\r\n'
            elif line_endings == 'mac':
                delimiter = '\r'
            elif line_endings == 'linux':
                delimiter = '\n'
            else:
                delimiter = '\n'
            contents = self.view.substr(self.view.full_line(self.view.sel()[0]))
            o = Organizer(contents, delimiter, project_modules)
            new_content = o.reorganize()
            self.view.replace(edit, r=self.view.full_line(self.view.sel()[0]), text=new_content)
            sublime.status_message('Imports have been formatted.')
        except Exception:
            sublime.error_message(traceback.format_exc())
            raise
