import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp, db
from modelos import Paciente,Usuario
from django.utils import simplejson
from templateCode.sesion import Sesion
from busquedausuario import BusquedaUsuario
from ajax.graborelaciones import GraboRelaciones

class GraboPaciente(webapp.RequestHandler):
    def ExistePaciente(self,Usuario):
	bRetorno=True
	if self.instanciaPaciente(Usuario) ==None:
		bRetorno=False
	return bRetorno
    
    def instanciaUsuarioPaciente(self,Usuario):
        busqueda=BusquedaUsuario()
        Usuario=str(Usuario).upper()
	usuario=None
        if busqueda.Busco(Usuario): #si existe el usuario
	    query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",Usuario)
	    usuario = query.fetch(1)
        for usr in usuario:
            usuario=usr
            break
        return usuario
    
    def instanciaPaciente(self, Usuario):
	busqueda=BusquedaUsuario()
        Usuario=str(Usuario).upper()
	instancia=None
	if busqueda.Busco(Usuario): #si existe el usuario
	    query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",Usuario)
	    usuario = query.fetch(1)
            query=None
	    for usr in usuario: #solo debe ser uno - ver fetch-
		query = db.GqlQuery("SELECT * FROM Paciente WHERE usuario = :1 ",
		usr)
	    pc = query.fetch(1)
	    for paciente in pc:
		instancia=paciente
		break
	return instancia    
    
    def UpdateDatos(self,Usuario):
        paciente=self.instanciaPaciente(Usuario)
        Usuario=str(Usuario).upper()
	if paciente==None:
	    self.AltaPaciente()
	else:
	    nombre=self.request.get('nombre')
            paciente.nombre = nombre
	    paterno=self.request.get('paterno')
            paciente.paterno = paterno
	    materno=self.request.get('materno')
            paciente.materno = materno
            paciente.fecha_nacimiento = self.request.get('fecha_nacimiento')
            paciente.estatura =float(self.request.get('estatura'))
            paciente.correo=self.request.get('correo')
            paciente.peso = float(self.request.get('peso'))
	    db.put(paciente)    
	return False
    
    def AltaPaciente(self):
        user=Usuario(usuario=str(self.request.get('usuario')).upper(),
                    password=str(self.request.get('password')).upper())
        paciente=Paciente()
        paciente.usuario=user.put()
	nombre=str(self.request.get('nombre')).upper()
        paciente.nombre = nombre
	paterno=self.request.get('paterno')#lo grabo en variables para evitar problemas con el encodig
	paciente.paterno = paterno
	materno=self.request.get('materno');
	paciente.materno =  materno
	paciente.fecha_nacimiento = self.request.get('fecha_nacimiento')
	paciente.estatura =float(self.request.get('estatura'))
	paciente.correo=self.request.get('correo')
	paciente.peso = float(self.request.get('peso'))
        paciente.telefono = self.request.get('telefono')
        paciente.celular = self.request.get('celular')
        paciente.direccion = self.request.get('direccion')
        paciente.put()
        relacion=GraboRelaciones()
        dr=self.request.get('dr')
        relacion.Grabar(dr,user.usuario)
        return False

    def post(self): 
	'''import sys 
	reload(sys)
	sys.setdefaultencoding("latin_1")'''
	sess = Sesion()	
	self.UpdateDatos(sess.getUser())
        return False

		
class GraboCookiePaciente(webapp.RequestHandler):
    def instanciaPaciente(self, Usuario):
        Usuario=str(Usuario).upper()
	busqueda=BusquedaUsuario()
        key=0
	instancia=None        
	busqueda=BusquedaUsuario()	
	if busqueda.Busco(Usuario): #si existe el usuario
	    query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",Usuario)
	    usuario = query.fetch(1)
	    query=None
	    for usr in usuario: #solo debe ser uno - ver fetch-
		query = db.GqlQuery("SELECT * FROM Paciente WHERE usuario = :1 ",
		usr)
	    pc = query.fetch(1)
	    for paciente in pc:
		instancia=paciente		
            try:#cuando no existe marca excepcion "'NoneType' object has no attribute 'key'"
                key=instancia
                if key==None:
                    key=0
            except:
                key=0
	return key
    
    def post(self):
        self.session=Sesion()
        usuario=self.request.get('usuario')
        if len(usuario)>0:                
            self.session.store(user=str(self.instanciaPaciente(usuario)),COOKIE_NAME_2="pacn")
        else:
            self.session.logout(COOKIE_NAME_2="pacn")
        return False
	
