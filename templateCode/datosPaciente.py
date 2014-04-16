import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ext import djangoforms
from modelos import Paciente, Usuario
from absolutePath import AbsolutePath
from sesion import Sesion
from ajax.grabopaciente import GraboPaciente
from citas import Citas
from decoratorlogin import loginRequerido

class DatosPaciente(webapp.RequestHandler):
	@loginRequerido
	def get(self):
		"""ABC de altas de doctores"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()
		pathtemplate = os.path.join(path, 'templates/datospaciente.html')
		
		session=Sesion()
		paciente=GraboPaciente()
		cita=Citas() #para obtener la lista de dr relacionados con el usuario
		doctores=cita.ObtenerDoctores(session.getUser())
		
		if paciente.ExistePaciente(session.getUser()):
			template_values = {
			'FormaPaciente' :FormaPaciente(instance=paciente.instanciaPaciente(session.getUser())),
			'existe': False,
			'doctores':doctores,
			}
		else:
			template_values = {
				'FormaPaciente' :FormaPaciente(),
				'existe': True,
				'doctores':doctores,
			}
		self.response.out.write(template.render(pathtemplate, template_values))

class FormaPaciente(djangoforms.ModelForm):
	class Meta: #usada para definir que modelo va a utilizar la forma
		model = Paciente
		exclude = ['usuario']

