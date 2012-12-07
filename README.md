sublime_python_imports
======================

Sublime Text 2 plugin for organizing imports in your Python source code. 
Rules are described by Guido here: http://www.python.org/dev/peps/pep-0008/#imports


Example 
========
Input
--------

```
  import sys
  import project.module1
  import os
  import django.contrib
  import django.admin
```

When selecting and pressing Cmd + Shift + I  it will format this like this:

Output
-------

```
  import os
  import sys
  
  import django.admin
  import django.contrib
  
  import project.module1
```

Installation
============

Use Sublime Text 2 Package manager. Look for python_imports_sorter
