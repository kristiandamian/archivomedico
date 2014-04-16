from google.appengine.ext import db
from google.appengine.ext import blobstore

class Usuario(db.Model):
        usuario= db.StringProperty()
        password=db.StringProperty()
	correo=db.EmailProperty()
       	creado = db.DateTimeProperty(auto_now=True) #dia y hora de creacion
       	
        def __unicode__(self):
                return self.usuario

class Acceso(db.Model):
        usuario= db.ReferenceProperty(Usuario)
        creado = db.DateTimeProperty(auto_now=True) #dia y hora de creacion
        fechaFinAcceso=db.DateTimeProperty()

class Paciente(db.Model):
        usuario = db.ReferenceProperty(Usuario)
	nombre = db.StringProperty()
	paterno = db.StringProperty()    
	materno = db.StringProperty()
	fecha_nacimiento = db.StringProperty()
	telefono= db.StringProperty()
	celular = db.StringProperty()
	direccion= db.StringProperty()	
	estatura = db.FloatProperty()
	correo=db.EmailProperty()
	peso = db.FloatProperty()

        def __unicode__(self):
                return self.nombre + " " + self.paterno + " " + self.materno	

class Doctor(db.Model):
        usuario = db.ReferenceProperty(Usuario)
	nombre = db.StringProperty()
	paterno = db.StringProperty()    
	materno = db.StringProperty()
	direccion=db.StringProperty()
	telefono=db.StringProperty()
	web=db.StringProperty()
	especialidad=db.StringProperty()
	correo=db.EmailProperty()
	
        def __unicode__(self):
                return "Dr." + self.nombre + " " + self.paterno + " " + self.materno

class Secretaria(db.Model):
	usuario = db.ReferenceProperty(Usuario)
	#doctor = db.ReferenceProperty(Doctor)
	nombre = db.StringProperty()
	paterno = db.StringProperty()    
	materno = db.StringProperty()
	telefono= db.StringProperty()
	celular = db.StringProperty()
	direccion= db.StringProperty()
        def __unicode__(self):
                return self.nombre + " " + self.paterno + " " + self.materno

class Relacion (db.Model):
	doctor=db.ReferenceProperty(Doctor)
	usuario=db.ReferenceProperty(Usuario)#secretaria o paciente

	
class Cita(db.Model):
        fecha= db.StringProperty()
        horaInicial= db.DateTimeProperty()
        horaFinal= db.DateTimeProperty()        
        duracion = db.IntegerProperty()
        doctor=db.ReferenceProperty(Doctor) 
        paciente=db.ReferenceProperty(Paciente)
	pacientenuevo=db.StringProperty()

class Consulta(db.Model):
        doctor=db.ReferenceProperty(Doctor) 
        usuario=db.ReferenceProperty(Usuario)
	creado = db.DateTimeProperty(auto_now=True) #dia y hora de la consulta

        def __unicode__(self):
                return self.usuario.nombre+" "+ self.usuario.paterno+" "+  self.usuario.materno+"-"+ self.doctor.nombre+" "+ self.doctor.paterno+" "+  self.doctor.materno

class Sintoma(db.Model):
        consulta=db.ReferenceProperty(Consulta) 
        nombre = db.StringProperty()
        
        def __unicode__(self):
                return self.nombre 

class Diagnostico(db.Model):
        consulta=db.ReferenceProperty(Consulta)         
        nombre = db.StringProperty(multiline=True)
	creado = db.DateTimeProperty(auto_now=True) #dia y hora de la consulta

        def __unicode__(self):
                return self.nombre         

class Receta(db.Model):
        consulta=db.ReferenceProperty(Consulta)
        prescripcion = db.StringProperty()        
        def __unicode__(self):
                return self.prescripcion

class Estudio(db.Model):
	nombre = db.StringProperty()
        paciente=db.ReferenceProperty(Paciente)
	
	parametro= db.StringProperty()
	resultado= db.StringProperty()
	limiteReferencia= db.StringProperty()	
	archivo=blobstore.BlobReferenceProperty()
	creado=db.DateTimeProperty(required=True, auto_now_add=True)
	
        def __unicode__(self):
                return self.nombre 


        
