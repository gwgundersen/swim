#!/home1/gregoso6/public_html/swim/venv/bin/python

from flup.server.fcgi import WSGIServer
from swim import app as application

WSGIServer(application).run()
