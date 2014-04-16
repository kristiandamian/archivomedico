import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath

class menuMovil(webapp.RequestHandler):
	def get(self):
		"""MenuPrincipal Movil"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate = os.path.join(path, 'templates/mobile//m_menu.html')
 
		self.response.out.write(template.render(pathtemplate, None))

