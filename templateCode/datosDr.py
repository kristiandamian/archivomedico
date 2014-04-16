import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from ext import djangoforms
from modelos import Doctor
from absolutePath import AbsolutePath
from sesion import Sesion
from ajax.validodr import ValidoDoctor
from decoratorlogin import loginRequerido, RequierePermisosDoctor

class DatosDr(webapp.RequestHandler):
	@loginRequerido
	@RequierePermisosDoctor
	def get(self):
		"""ABC de altas de doctores"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate = os.path.join(path, 'templates/datosdr.html')
		
		template_values =None
		session=Sesion()
		dr=ValidoDoctor()
		if dr.ExisteDr(session.getUser()):
			template_values = {
				'FormaDoctor' :FormaDoctor(instance=dr.instanciaDoctor(session.getUser())),
				
			}
		else:
			template_values = {
				'FormaDoctor' :FormaDoctor(),				
			}
		self.response.out.write(template.render(pathtemplate, template_values))

class FormaDoctor(djangoforms.ModelForm):
	class Meta: #usada para definir que modelo va a utilizar la forma
			model = Doctor
			exclude=['usuario']
