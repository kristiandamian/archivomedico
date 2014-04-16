import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp, db
from modelos import Secretaria,Usuario
from django.utils import simplejson
from templateCode.sesion import Sesion
from ajax.graborelaciones import GraboRelaciones
from busquedausuario import BusquedaUsuario

class GraboSecretaria(webapp.RequestHandler):
    def ExisteSecretaria(self,Usuario):
	bRetorno=True
	if self.instanciaSecretaria(Usuario) ==None:
		bRetorno=False
	return bRetorno
    
    def instanciaSecretaria(self, Usuario):
	busqueda=BusquedaUsuario()
	Usuario=str(Usuario).upper()
	instancia=None
	if busqueda.Busco(Usuario): #si existe el usuario
	    query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",Usuario)
	    usuario = query.fetch(1)
	    query=None
	    for usr in usuario: #solo debe ser uno - ver fetch-
		query = db.GqlQuery("SELECT * FROM Secretaria WHERE usuario = :1 ",usr)
		break
	    pc = query.fetch(1)
	    for secretaria in pc:
		instancia=secretaria
		break
	return instancia    
    
    def UpdateDatos(self,Usuario):
	Usuario=str(Usuario).upper()
        secre=self.instanciaSecretaria(Usuario)
	if secre==None:
	    self.AltaSecretaria()
	else:
	    nombre=self.request.get('nombre')#str(self.request.get('nombre')).upper()
            secre.nombre = nombre
	    paterno=self.request.get('paterno')
            secre.paterno = paterno
	    materno=self.request.get('materno')
            secre.materno = materno
	    telefono=self.request.get('telefono')
	    secre.telefono= telefono
	    celular=self.request.get('celular')
	    secre.celular= celular
	    direccion=self.request.get('direccion')
	    secre.direccion= direccion
	    doctores=self.request.get('doctores')
	    db.put(secre)
	    self.AltaRelaciones(doctores,Usuario)
	return False
    
    def AltaSecretaria(self):
        user=Usuario(usuario=str(self.request.get('usuario')).upper(),
                    password=str(self.request.get('password')).upper())
	doctores=self.request.get('doctores')
        secre=Secretaria()
        secre.usuario=user.put()
        nombre=self.request.get('nombre')#str(self.request.get('nombre')).upper()
	secre.nombre = nombre
	paterno=self.request.get('paterno')
        secre.paterno = paterno
	materno=self.request.get('materno')
        secre.materno = materno
	telefono=self.request.get('telefono')
	secre.telefono= telefono
	celular=self.request.get('celular')
	secre.celular= celular
	direccion=self.request.get('direccion')
	secre.direccion= direccion
        secre.put()
	self.AltaRelaciones(doctores,user.usuario)
        return False
    
    def AltaRelaciones(self,doctores,usuarioSecretaria):
	"""Doy de alta la relacion (la clase valida si es que ya existe y no lo graba)
	secretaria es el usuario tipo string
	doctores es un string en el formato ssss|ssss|ssss| donde el pipe es el separador del usuario
	"""
	doctores=str(doctores).split("|")
	graborelaciones=GraboRelaciones()
	for dr in range(0,len(doctores)-1):
	    graborelaciones.Grabar(doctores[dr],usuarioSecretaria)
	return False

    def post(self):        
	sess = Sesion()	
	self.UpdateDatos(sess.getUser())
        return False
