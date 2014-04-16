import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ext import djangoforms
from modelos import Secretaria, Usuario
from absolutePath import AbsolutePath
from sesion import Sesion
from ajax.grabosecretaria import GraboSecretaria
from decoratorlogin import loginRequerido, RequierePermisosDoctor, RequierePermisosSecretaria,RequierePermisosDoctoroSecretaria
from citas import Citas

class DatosSecretaria(webapp.RequestHandler):
	@loginRequerido
	@RequierePermisosDoctoroSecretaria	
	def get(self):
		"""ABC de altas de doctores"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate = os.path.join(path, 'templates/datossecretaria.html')
		
		session=Sesion()
		secre=GraboSecretaria()
		cita=Citas() #para obtener la lista de dr relacionados con el usuario
		doctores=cita.ObtenerDoctores(session.getUser())

		if secre.ExisteSecretaria(session.getUser()):
			template_values = {
				'FormaSecretaria' :FormaSecretaria(instance=secre.instanciaSecretaria(session.getUser())),
				'existe': None,
				'doctores':doctores,
			}
		else:
			template_values = {
				'FormaSecretaria' :FormaSecretaria(),
				'existe': 1,
				'doctores':doctores,
			}
		self.response.out.write(template.render(pathtemplate, template_values))

class FormaSecretaria(djangoforms.ModelForm):
	class Meta: #usada para definir que modelo va a utilizar la forma
		model = Secretaria
		exclude = ['usuario']

