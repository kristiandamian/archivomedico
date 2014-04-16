import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp, db
from modelos import Doctor,Usuario
from django.utils import simplejson
from templateCode.sesion import Sesion
from busquedausuario import BusquedaUsuario
from validodr import ValidoDoctor

class GraboDR(webapp.RequestHandler):

    def UpdateDatos(self,Usuario):
	validoDr=ValidoDoctor()
	Usuario=str(Usuario).upper()
        doctor=validoDr.instanciaDoctor(Usuario)
	if doctor==None:
	    self.AltaDatos(Usuario)
	else:
	    doctor.nombre = self.request.get('nombre')
	    doctor.paterno = self.request.get('paterno')   
	    doctor.materno = self.request.get('materno')
	    doctor.direccion = self.request.get('direccion')
	    doctor.web =self.request.get('web')
	    doctor.correo=self.request.get('correo')
	    doctor.telefono=self.request.get('telefono')
	    doctor.especialidad = self.request.get('especialidad')
	    db.put(doctor)    
	return False
    
    def AltaDatos(self,usuario):
	usuario=str(usuario).upper()
	query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",
                            usuario)
	res=None
        for res in query:
	    user=res
	    break
        doctor=Doctor()
        doctor.usuario=user
        doctor.nombre = str(self.request.get('nombre')).upper()
	doctor.paterno = str(self.request.get('paterno')).upper()
	doctor.materno = str(self.request.get('materno')).upper()
	doctor.direccion = self.request.get('direccion')
	doctor.especialidad = self.request.get('especialidad')
	doctor.web =self.request.get('web')
	doctor.correo=self.request.get('correo')
	doctor.telefono=self.request.get('telefono')
        doctor.put()
	return False
    
    def post(self):
	sess = Sesion()
	if sess.load():
	    self.UpdateDatos(sess.getUser())
        return False
