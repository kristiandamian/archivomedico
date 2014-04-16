import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp

class signMobile(webapp.RequestHandler):
    def post(self):
        #todo validar si existe el usuario
        validUser=True
        if validUser:
            self.redirect("/menumovil")
        else:
            self.redirect("/errormovil")
        return None
