import cgi
import wsgiref.handlers
import os
from datetime import date
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath

class errorMovil(webapp.RequestHandler):
	def get(self):
		"""ABC de altas de doctores"""	 
		error="Usuario o password incorrectos"
		template_values={
                                'error':error,
                        }
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate = os.path.join(path, 'templates/mobile/m_error.html')
		self.response.out.write(template.render(pathtemplate, template_values))

