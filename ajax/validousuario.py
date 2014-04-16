import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from modelos import Usuario
from django.utils import simplejson
from google.appengine.ext import db
from templateCode.sesion import Sesion
from validodr import ValidoDoctor

class ValidoUsuario(webapp.RequestHandler):
    def AgregoUsuario(self):
        user=Usuario(usuario='prueba',password='123')
        user.put()
    
    def InstaciaUsuario(self,usuario):
	usuario=str(usuario).upper()
        query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",usuario)
	resultados = query.fetch(1)
	Usuario=None
        for res in resultados:
            Usuario=res
            break
	return Usuario
	
    def post(self):
        cantidad=0
        #self.AgregoUsuario()
        self.session=Sesion()
	self.session.logout()

        query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 and password= :2",
                            str(self.request.get('usuario')).upper(),
                            str(self.request.get('password')).upper(),)
        resultados = query.fetch(1)             
        for res in resultados:
            cantidad=1
            break

        if cantidad>=1:
            self.session.store(str(self.request.get('usuario')).upper())
        else:
            cantidad=0 #NO hay sesion, marco un error (que el usuario no existe)
            
        jsondata=[]
        jsondic={}
        jsondic["user"]=cantidad
        jsondata=[jsondic]
        self.response.out.write(simplejson.dumps(jsondata))
        return jsondata

class ValidoUsuarioDr(webapp.RequestHandler):
    def post(self):
	usuario=str(self.request.get('usuario')).upper()
	dr=ValidoDoctor()
	doctor=dr.instanciaDoctor(usuario)
	sRetorno="failure"
	jsondata=[]
        jsondic={}
	if doctor!=None:
	    sRetorno=doctor.usuario.usuario+"|Dr. "+ doctor.nombre+ " "+doctor.paterno+" "+doctor.materno
        jsondic["user"]=sRetorno
        jsondata=[jsondic]
        self.response.out.write(simplejson.dumps(jsondata))
        return jsondata
	