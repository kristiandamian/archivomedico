import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from movil.mobile import mobileBrowser
from absolutePath import AbsolutePath

from sesion import Sesion

class Login(webapp.RequestHandler):
	def get(self):
		"""ABC de altas de doctores"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate=None

		#self.session=Sesion()
		#self.session.logout()
		#self.session.store('Kristian')
		
		if mobileBrowser(self):
        		pathtemplate = os.path.join(path, 'templates/mobile/m_login.html')
        	else:
        		pathtemplate = os.path.join(path, 'templates/login.html')
        	self.response.out.write(template.render(pathtemplate, None))

class Logout(webapp.RequestHandler):
       	def get(self):
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate=None
		self.session=Sesion()
                self.session.logout()
                self.redirect("/")

