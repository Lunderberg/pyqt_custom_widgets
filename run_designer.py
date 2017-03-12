#!/usr/bin/env python3

import os
import subprocess
import sys

def append_path(varname, new_path):
    if (varname not in os.environ or
        not os.environ[varname]):
        os.environ[varname] = new_path
    else:
        os.environ[varname] += ':' + new_path

base = os.path.dirname(__file__)
append_path('PYQTDESIGNERPATH',
            os.path.join(base, 'designer-qt4_plugins'))
append_path('PYTHONPATH', base)

subprocess.call(['designer-qt4'] + sys.argv[1:])
