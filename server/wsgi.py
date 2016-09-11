#!/usr/bin/python
import sys
import os
import logging

logging.basicConfig(stream=sys.stderr)

# path of project is the directory containing the wsgi file
project = os.path.dirname(__file__)
path = os.path.dirname(project)
if project not in sys.path:
    sys.path.insert(0,project)

from __init__ import app as application
application.secret_key = 'rer236et7wy27ye327'
