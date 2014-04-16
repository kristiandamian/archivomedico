import cgi
import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath

class Cancelar (webapp.RequestHandler):
	def get(self):
                MyPath=AbsolutePath()
		ABSpath=MyPath.getAbsolutePath()
		path = os.path.join(ABSpath, 'templates/cancelar.html')	
		self.response.out.write(template.render(path, None))

