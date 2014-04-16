import cgi
import wsgiref.handlers
import os
import datetime as dt
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from ext import djangoforms
from modelos import Cita, Relacion
from decoratorlogin import loginRequerido, RequierePermisosDoctor
from absolutePath import AbsolutePath
from sesion import Sesion
from ajax.busquedausuario import BusquedaUsuario
from ajax.validodr import ValidoDoctor
from ajax.validousuario import ValidoUsuario

class Citas(webapp.RequestHandler):
        Periodos=0
        Duracion=0
	horaInicial="7:00"
        
        def __init__(self):
                self.Periodos=2  #Cuantos periodos de N minutos hay en una hora (Duracion Cita/60)
                self.Duracion=30 #Cuanto Dura la cita
                
        @loginRequerido	
        def get(self):
		"""ABC de Citas"""
		MyPath=AbsolutePath()
		path=MyPath.getAbsolutePath()

		pathtemplate = os.path.join(path, 'templates/citas.html')
		fecha=str(dt.date.today().day)+"/"+str(dt.date.today().month)+"/"+str(dt.date.today().year)[2:]
		fechaVer2=str(dt.date.today().day)+"-"+str(dt.date.today().month)+"-"+str(dt.date.today().year)
		sess = Sesion()
		doctores=self.ObtenerDoctores(sess.getUser())
		template_values={
                                'horarios':self.Agenda(doctores[0].usuario.usuario,fecha),#self.horario(),
				'doctores':doctores,
                                'hoy':fechaVer2,
				#'citas':self.Citas(doctores[0].usuario.usuario,fecha),								
                        }
		self.response.out.write(template.render(pathtemplate, template_values))

	def horario(self,horarioMilitar=True):
		"""Genero el horario para la tabla de citas"""
                hora=0
                Retorno=[]   #Hora inicial,Hora Final
                for x in range(7,22): #
                        for y in range(0,self.Periodos):
                                if x>12: 
                                        hora=x-12
                                else:
                                        hora=x
                                minuto=y*self.Duracion
                                min="00"
                                if minuto!=0:
                                        min=str(minuto)
                                if horarioMilitar:
                                     horario=str(x)+":"+min   
                                else:
                                        horario=str(hora)+":"+min
                                Retorno.append(horario)
                return Retorno

	def ObtenerDoctores(self,usuario):
		"""Obtengo la lista de doctores que estan relacionados con un usuario"""
		instanciaUsuario=ValidoUsuario()
		Usuario=instanciaUsuario.InstaciaUsuario(usuario)
		lRetorno=[]
		if Usuario!=None: #si existe el usuario
			query = db.GqlQuery("SELECT * FROM Relacion WHERE usuario = :1 ", Usuario)
			for doctor in query:		
				lRetorno.append(doctor.doctor)
		if lRetorno==[]: #es un doctor?
			doctor=self.instanciaDoctor(usuario)
			if doctor!=None:
				lRetorno.append(doctor)
		return lRetorno
		
	def instanciaDoctor(self,Usuario):
		busqueda=BusquedaUsuario()
		instanciadr=None
		if busqueda.Busco(Usuario): #si existe el usuario
		    query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",
				    Usuario)
		    usuario = query.fetch(1)
		    query=None
		    for usr in usuario: #solo debe ser uno - ver fetch-
			query = db.GqlQuery("SELECT * FROM Doctor WHERE usuario = :1 ",
			usr.key())
		    dr = query.fetch(1)
		    for doctor in dr:
			instanciadr=doctor
			break
		return instanciadr

	def Citas(self,dr,fecha):		
		lRetorno=[]		
		validoDr=ValidoDoctor()
		doctor=validoDr.instanciaDoctor(dr)
		if doctor==None:
			lRetorno=False
		else:
			query = db.GqlQuery("SELECT * FROM Cita WHERE doctor = :1 and fecha= :2",
					doctor,fecha)
			for res in query:
				dic={}
				fecha=str(res.horaInicial.day)+"/"+str(res.horaInicial.month)+"/"+str(res.horaInicial.year)[-2:]
				minutos=res.horaInicial.minute
				if minutos==0:
					minutos="00"
				else:
						minutos=str(minutos)
				horainicial=str(res.horaInicial.hour)+":"+minutos
				dic["horainicial"]=horainicial
				inicio=fecha+" "+self.horaInicial
				fechainicial=dt.datetime.strptime(inicio, "%d/%m/%y %H:%M")
				diff=((res.horaInicial-fechainicial)/60)/self.Duracion
				diffFinal=((res.horaFinal-fechainicial)/60)/self.Duracion
				dic["posicion"]=diff.seconds #posicion en la tabla
				if res.duracion==None:
					dic["renglones"]=1
				else:
					dic["renglones"]=int(res.duracion) #diffFinal-diff.seconds#cuantos renglones seran 
				#dic["inicio"]=res.horaInicial
				#dic["fin"]=res.horaFinal
				if res.pacientenuevo==None:
					dic["paciente"]=res.paciente.nombre+" "+res.paciente.paterno+" "+res.paciente.materno
				else:
					dic["paciente"]=res.pacientenuevo					
				lRetorno.append(dic)
		#my mock object :D
		#dic={}
		#dic["posicion"]=2
		#dic["renglones"]=2
		#dic["paciente"]="Juan Camaney"
		#dic["horainicial"]="12:00"
		#lRetorno.append(dic)
		#dic={}
		#dic["posicion"]=2
		#dic["renglones"]=3
		#dic["paciente"]="pepe el toro"
		#dic["horainicial"]="8:00"
		#lRetorno.append(dic)
		#end of my mock object
		return lRetorno
	
	def Agenda(self,dr,fecha):
		lRetorno=[]
		horas=self.horario()
		citas=self.Citas(dr,fecha)
		for hora in horas:			
			dHora={}
			if citas != []: #si hay al menos alguna cita				
				for cita in citas:				
					if cita["horainicial"]==hora:
						dHora["hora"]=hora					
						dHora["renglones"]=cita["renglones"]
						dHora["paciente"]=cita["paciente"]
						break
					else:
						dHora["hora"]=hora					
						dHora["renglones"]=1
						dHora["paciente"]=""
			else: #si no hay citas, esto evita que se ponga en blanco la tabla
				dHora["hora"]=hora					
				dHora["renglones"]=1
				dHora["paciente"]=""
			lRetorno.append(dHora)
		return lRetorno

