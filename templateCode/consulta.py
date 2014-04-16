import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath
from decoratorlogin import loginRequerido, RequierePermisosDoctor

class Consulta(webapp.RequestHandler):
	@loginRequerido
	@RequierePermisosDoctor
	def get(self):
		"""ABC de altas de doctores"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate = os.path.join(path, 'templates/consulta.html') 
		self.response.out.write(template.render(pathtemplate, None))

