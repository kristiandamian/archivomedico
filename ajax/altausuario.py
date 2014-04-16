import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from modelos import Usuario
from django.utils import simplejson

class AltaUsuario(webapp.RequestHandler):

    
    def post(self):
        user=Usuario(usuario=str(self.request.get('usuario')).upper(),
                     password=str(self.request.get('password')).upper())
        user.put()
        return False
