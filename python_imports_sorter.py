#!/usr/bin/python

""" Sublime plugin: python_imports_sorter
Author: marcin.kliks@gmail.com
License: MIT
Version 0.1
https://github.com/vi4m/sublime_python_imports
"""

import sublime_plugin
import sublime

from organizer import Organizer


class SortImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            project_modules = sublime.Settings.get('project_modules', [])
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
            edit = self.view.begin_edit()
            contents = self.view.substr(self.view.full_line(self.view.sel()[0]))
            o = Organizer(contents, delimiter, project_modules)
            new_content = o.reorganize()
            self.view.replace(edit, self.view.full_line(self.view.sel()[0]), new_content)
            self.view.end_edit(edit)
            sublime.status_message('Imports have been formatted.')
        except Exception as e:
            sublime.error_message(e)

