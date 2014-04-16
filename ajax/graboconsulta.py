import cgi
import wsgiref.handlers
from google.appengine.ext import webapp, db
from modelos import Consulta,Paciente,Usuario, Sintoma, Diagnostico, Receta
from django.utils import simplejson
from templateCode.sesion import Sesion
from validodr import ValidoDoctor
from grabopaciente import GraboPaciente

class GraboConsulta(webapp.RequestHandler):
    def get(self,req):
        sess = Sesion()
        usuario=sess.getUser()
        validoDr=ValidoDoctor()
        dr=validoDr.instanciaDoctor(usuario)
	instPac=GraboPaciente()
        usuario=instPac.instanciaUsuarioPaciente(self.request.get("paciente"))
        consulta=Consulta()
        consulta.doctor=dr
        consulta.usuario=usuario
        consulta.put()
	jsondic={}
        jsondata=[]
        jsondic["id"]=consulta.key().id()
        jsondata=[jsondic]
	self.response.out.write(simplejson.dumps(jsondata))
	
class GraboSintoma(webapp.RequestHandler):
    '''Evito que se dupliquen los sintomas al darle grabar dos veces en la pagina "Consultas" '''
    def BorroSintomas(self,id,sint):
	consulta=Consulta.get_by_id(int( self.request.get("id")))
	query = db.Query(Sintoma)
	query=Sintoma.all()
	query=query.filter("consulta =",consulta)
	for sintoma in query:
	    if sint==sintoma.nombre:
		sintoma.delete()
    
    def post(self):
	self.BorroSintomas(int( self.request.get("id")),self.request.get("sintoma"))
	consulta=Consulta.get_by_id(int( self.request.get("id")))
	sintoma=Sintoma()
	sintoma.consulta=consulta
	sintoma.nombre=self.request.get("sintoma")
	sintoma.put()
	return False		

class GraboDiagnostico(webapp.RequestHandler):
    '''Evito que se dupliquen los Diagnosticos al darle grabar dos veces en la pagina "Consultas" '''
    def BorroDiagnosticos(self,id,diag):
	consulta=Consulta.get_by_id(int( self.request.get("id")))
	query = db.Query(Diagnostico)
	query=Diagnostico.all()
	query=query.filter("consulta =",consulta)
	for diagnostico in query:
	    if diag==diagnostico.nombre:
		diagnostico.delete()
    
    def post(self):
	self.BorroDiagnosticos(int( self.request.get("id")),self.request.get("diagnostico"))
	consulta=Consulta.get_by_id(int( self.request.get("id")))
	diagnostico=Diagnostico()
	diagnostico.consulta=consulta
	diagnostico.nombre=self.request.get("diagnostico")
	diagnostico.put()
	return False
    
class GraboReceta(webapp.RequestHandler):
    '''Evito que se dupliquen las recetas al darle grabar dos veces en la pagina "Consultas" '''
    def BorroRecetas(self,id,prescripcion):
	consulta=Consulta.get_by_id(int( self.request.get("id")))
	query = db.Query(Receta)
	query=Receta.all()
	query=query.filter("consulta =",consulta)
	for receta in query:
	    if(prescripcion==receta.prescripcion):
		receta.delete()
	    
    def post(self):
	self.BorroRecetas(int( self.request.get("id")),self.request.get("prescripcion"))
	consulta=Consulta.get_by_id(int( self.request.get("id")))
	receta=Receta()
	receta.consulta=consulta
	receta.prescripcion=self.request.get("prescripcion")	
	receta.put()
	return False	    
     