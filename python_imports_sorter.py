#!/usr/bin/python

""" Sublime plugin: python_imports_sorter
Author: marcin.kliks@gmail.com
License: MIT
Version 0.2
https://github.com/vi4m/sublime_python_imports
"""

import traceback

from organizer import Organizer
import sublime
import sublime_plugin


class SortImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            settings = sublime.load_settings("python_imports_sorter.sublime-settings")
            project_modules = settings.get('project_modules', [])
            sublime.status_message(('Formatting imports...'))
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
            sublime.status_message(('Imports have been formatted.'))
        except Exception:
            sublime.error_message((traceback.format_exc()))
            raise
