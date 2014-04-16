import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath

class HistorialMovil(webapp.RequestHandler):
	def get(self):
            MyPath=AbsolutePath()
	    path=MyPath.getAbsolutePath()
	    pathtemplate = os.path.join(path, 'templates/mobile/historial.html')
 
	    self.response.out.write(template.render(pathtemplate, None))