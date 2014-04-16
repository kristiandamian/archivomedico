import cgi
import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath
from decoratorlogin import loginRequerido

class MainPage (webapp.RequestHandler):
	@loginRequerido
	def get(self):
		"""Muestro la pantalla principal con solo las marcas de referencia"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate = os.path.join(path, 'templates/inicio.html')	
		self.response.out.write(template.render(pathtemplate, None))
