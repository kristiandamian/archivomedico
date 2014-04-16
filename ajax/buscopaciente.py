import cgi
import wsgiref.handlers
import os
from google.appengine.ext import webapp, db
from modelos import Paciente
from django.utils import simplejson

class BuscoPaciente(webapp.RequestHandler):
    def addKey(self,diccionario,key,data):
        diccionario={key:data}
        return diccionario    
    
    def post(self):
        nombre=self.request.get('nombre')
        paterno=self.request.get('paterno')
        materno=self.request.get('materno')
        query = db.Query(Paciente)        
    
        if len(nombre)>0:
            query.filter("nombre =",nombre)
        if len(paterno)>0:
            query.filter("paterno =",paterno)
        if len(materno)>0:
            query.filter("materno =",materno)
        
        jsondic={}
        jsondata=[]
        nombres=[]
        jsondic['cantidad']=query.count()
        x=0
        for res in query:
            nombre=res.nombre+'|'+res.paterno+'|'+res.materno+'|'+res.fecha_nacimiento+"|"+res.usuario.usuario
            nombres+=[nombre]
            x=x+1
        jsondic['nombres']=nombres
        jsondata+=[jsondic]        
        self.response.out.write(simplejson.dumps(jsondata))
        return False
