import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp

class LogoutMovil(webapp.RequestHandler):
    def get(self):
        self.redirect("/")

