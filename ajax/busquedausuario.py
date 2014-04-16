import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from modelos import Usuario
from django.utils import simplejson
from google.appengine.ext import db

class BusquedaUsuario(webapp.RequestHandler):
    
    def Busco(self,usuario):
        usuario=str(usuario).upper()
        query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",
                            usuario)
        resultados = query.fetch(1)
        cantidad=0
        for res in resultados:
            cantidad=1
            break
        return cantidad        
    
    def post(self):
        #query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",
        #                    self.request.get('usuario'))
        #resultados = query.fetch(1)     
        ##user=Usuario.all()
        #cantidad=0
        #for res in resultados:
        #    cantidad=1
        #    break
        cantidad=self.Busco(self.request.get('usuario'))
        jsondata=[]
        jsondic={}
        jsondic["user"]=cantidad
        jsondata=[jsondic]
        self.response.out.write(simplejson.dumps(jsondata))
        return jsondata
