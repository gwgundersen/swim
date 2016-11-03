#!/home1/gregoso6/public_html/glossary/venv/bin/python

from flup.server.fcgi import WSGIServer
from swimming import app as application

WSGIServer(application).run()
