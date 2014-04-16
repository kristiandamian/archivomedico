import cgi
import wsgiref.handlers
import os
import datetime as dt
from google.appengine.ext import webapp, db
from modelos import Doctor,Usuario,Cita
from django.utils import simplejson
from templateCode.sesion import Sesion
from templateCode.citas import Citas
from busquedausuario import BusquedaUsuario
from grabopaciente import GraboPaciente
from validodr import ValidoDoctor

class BorroCita(webapp.RequestHandler):
    def post(self):
	sess = Sesion()
	Usuario=self.request.get("dr")
	hora=str(self.request.get("hora"))
	fechaCita=self.request.get("fecha")
	
	fecha=fechaCita[0:2]+"/"+fechaCita[3:5]+"/"+fechaCita[8:]# fecha estilo DD/MM/YY
	
	if sess.load():
            self.BorrarCita(Usuario,hora,fecha)
	    
        citas=Citas()	
	#hoy=str(dt.date.today().day)+"/"+str(dt.date.today().month)+"/"+str(dt.date.today().year)[2:]
	jsondata=citas.Agenda(Usuario,fecha)
	self.response.out.write(simplejson.dumps(jsondata))
	return jsondata

    def BorrarCita(self,usuario,hora,fecha):
        validoDr=ValidoDoctor()
	doctor=validoDr.instanciaDoctor(usuario)	    
	#fecha=str(dt.date.today().day)+"/"+str(dt.date.today().month)+"/"+str(dt.date.today().year)[2:]
        inicio=fecha+" "+hora
        fechainicial=dt.datetime.strptime(inicio, "%d/%m/%y %H:%M")
        if doctor != None:            
	    query=db.GqlQuery("SELECT * FROM Cita WHERE doctor = :1 and fecha=:2",doctor,fecha)
	    for cita  in query:
                if cita.horaInicial==fechainicial:
                    cita.delete()                    
                
class GraboCita(webapp.RequestHandler):    
#    def UpdateDatos(self,Usuario):
#	Usuario=str(Usuario).upper()
#	validoDr=ValidoDoctor()
#        doctor=validoDr.instanciaDoctor(Usuario)
#	if doctor!=None:
#	    sess=Sesion()
#	    if sess.load(COOKIE_NAME_2="pacn"):
#		key=db.Key(sess.getUser(COOKIE_NAME_2="pacn"))
#		pac=Paciente.gql("where __key__=:1",key)
#		paciente=pac.fetch(1)
#		AltaCita(doctor,paciente)
#	return False
    
    def AltaCita(self,dr,paciente,pacientenuevo,nombre,fecha,horainicial,horafinal,duracion):
        cita=Cita()
	validoDr=ValidoDoctor()
        doctor=validoDr.instanciaDoctor(dr)
	instPac=GraboPaciente()
        cita.doctor=doctor
	if not pacientenuevo:
	    cita.paciente=instPac.instanciaPaciente(paciente)
	else:
	    cita.pacientenuevo=nombre        
        time1=fecha +" "+ horainicial
        time2=fecha +" "+ horafinal
        FechaInicial= dt.datetime.strptime(time1, "%d/%m/%y %H:%M")
        FechaFinal= dt.datetime.strptime(time2, "%d/%m/%y %H:%M")
        cita.fecha=fecha
        cita.horaInicial=FechaInicial
	cita.duracion=int(duracion)
        cita.horaFinal=FechaFinal
        cita.put()
	return cita.key()
    
    def post(self):
	sess = Sesion()
	if sess.load():
	    dr=self.request.get('doctor')
	    pacientenuevo=self.request.get('pacientenuevo')
	    nombre=self.request.get('nombre')
	    paciente=self.request.get('paciente')
	    duracion=self.request.get('duracion')
	    if str(pacientenuevo)=="true":
		pacientenuevo=True
	    else:
		pacientenuevo=False
	    fecha=self.request.get('fecha')
	    campos=fecha.rsplit("-")
	    fecha=campos[0]+"/"+campos[1]+"/"+campos[2][2:]
	    horainicial=self.request.get('inicio')
	    horafinal=self.request.get('fin')
	    self.AltaCita(dr,paciente,pacientenuevo,nombre,fecha,horainicial,horafinal,duracion)
        return False

class BuscoCita(webapp.RequestHandler):
    def post(self):
	sess = Sesion()
	jsondata=[]
	Usuario=self.request.get("dr")
	if sess.load():
            validoDr=ValidoDoctor()
	    doctor=validoDr.instanciaDoctor(Usuario)	    
	    jsondic={}
	    cantidad=0
	    if doctor!=None:
		fecha=self.request.get('fecha')
		inicio=str(self.request.get('inicio'))				
		fin=str(self.request.get('fin'))
		cantidad=self.BuscoCita(fecha,inicio,fin,Usuario)
		
	    jsondic["citas"]=cantidad
	    jsondata=[jsondic]
	    self.response.out.write(simplejson.dumps(jsondata))
	return jsondata
    
    def BuscoCita(self,fecha,horaInicio,horaFin, Usuario):
	"""Busco que no exista una cita en la fecha y hora marcadas
	Fecha en el formato DD/MM/YY HH:MM
	doctor es una instancia de dicho modelo
	Devuelvo 0 cuando NO existe una cita"""
	validoDr=ValidoDoctor()
	doctor=validoDr.instanciaDoctor(Usuario)
	campos=fecha.rsplit("-")
	fecha=campos[0]+"/"+campos[1]+"/"+campos[2][2:]
	inicio=fecha+" "+horaInicio				
	fin=fecha+" "+horaFin	
	fechainicial=dt.datetime.strptime(inicio, "%d/%m/%y %H:%M")
	fechafinal=dt.datetime.strptime(fin, "%d/%m/%y %H:%M")
	#query = db.GqlQuery("SELECT * FROM Cita WHERE doctor = :1 and ((horaInicial<= :2 and horaFinal>:3) or (horaInicial< :4 and horaFinal>=:5))",
	#		doctor,fechainicial,fechainicial,fechafinal,fechafinal)
	cantidad=0
	if doctor != None:            
	    query=db.GqlQuery("SELECT * FROM Cita WHERE doctor = :1 and fecha=:2",doctor,fecha)    
	    for cita  in query:
		if (cita.horaInicial<=fechainicial and cita.horaFinal>fechainicial) or (cita.horaInicial<fechafinal and cita.horaFinal>= fechafinal):
		    cantidad=1 #hay una cita
		    if cantidad==1: #si hay un cita
			break #ya no busco
	else:
	    cantidad=-1    
	return cantidad
    

class ObtengoCitas(webapp.RequestHandler):
    def get(self,req):
	citas=Citas()
	dr=self.request.get("dr")	
	fechaCita=self.request.get("fecha")
	
	fecha=fechaCita[0:2]+"/"+fechaCita[3:5]+"/"+fechaCita[8:]# fecha estilo DD/MM/YY
	#hoy=str(dt.date.today().day)+"/"+str(dt.date.today().month)+"/"+str(dt.date.today().year)[2:]
	jsondata=citas.Agenda(dr,fecha)
	self.response.out.write(simplejson.dumps(jsondata))
	return jsondata
	
