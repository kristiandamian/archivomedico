import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from modelos import Usuario
from django.utils import simplejson
from google.appengine.ext import db
from templateCode.sesion import Sesion

class RenovarSubscripcion(webapp.RequestHandler):
    
    def post(self):
        sess = Sesion()
        cantidad=0        
        query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 and password= :2",
                            str(self.request.get('usuario')).upper(),
                            str(self.request.get('password')).upper(),)
        resultados = query.fetch(1)             
        for res in resultados:
            cantidad=1
            break
        if sess.load(COOKIE_NAME_2="armedPS"):#hay una sesion de seguridad(para evitar inyectar esta URL
            if cantidad>=1:
                #TODO grabar la renovacion
                pass
            sess.logout(COOKIE_NAME_2="armedPS")
        else:
            cantidad=0 #NO hay sesion, marco un error (que el usuario no existe)
        jsondata=[]
        jsondic={}
        jsondic["user"]=cantidad
        jsondata=[jsondic]
        self.response.out.write(simplejson.dumps(jsondata))
        return jsondata
