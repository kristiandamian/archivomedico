import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath

class BusquedaMovil(webapp.RequestHandler):
    def post(self):
        pass