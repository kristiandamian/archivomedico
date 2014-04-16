import cgi
import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath

class Subscribirse (webapp.RequestHandler):
	def get(self):
                MyPath=AbsolutePath()
		ABSpath=MyPath.getAbsolutePath()
		path = os.path.join(ABSpath, 'templates/subscribirse.html')	
		self.response.out.write(template.render(path, None))

