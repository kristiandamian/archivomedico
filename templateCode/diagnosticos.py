import os
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath
from modelos import Doctor, Paciente, Consulta, Diagnostico
from decoratorlogin import RequierePermisosDoctoroPaciente
from ajax.grabopaciente import GraboPaciente
from ajax.validodr import ValidoDoctor
from ajax.validousuario import ValidoUsuario
from sesion import Sesion

class Diagnosticos(webapp.RequestHandler):
    @RequierePermisosDoctoroPaciente
    def get(self):
        MyPath=AbsolutePath()
        path=MyPath.getAbsolutePath()
        pathtemplate = os.path.join(path, 'templates/diagnosticos.html')
        sess = Sesion()        
        template_values ={
                                'diagnosticos':self.ObtengoDiagnosticos(sess.getUser()),
                                'dr':self.EsDoctor(sess.getUser())
                        }
        self.response.out.write(template.render(pathtemplate, template_values))
    
    def EsDoctor(self,usuario):
        buscodr=ValidoDoctor()
        return buscodr.ExisteDr(usuario)
        
    def ObtengoDiagnosticos(self,usuario):
        buscopaciente=GraboPaciente()        
        lDiagonosticos=[]
        if buscopaciente.ExistePaciente(usuario):#es un paciente
            usuarioinstanciado=ValidoUsuario()
            usuario=usuarioinstanciado.InstaciaUsuario(usuario)
            query = db.GqlQuery("SELECT * FROM Consulta WHERE usuario = :1 ",usuario)	    
            consultas=query.fetch(10)
            for consulta in consultas:
                diagnostico={}
                fecha=str(consulta.creado.day)+"/"+str(consulta.creado.month)+"/"+str(consulta.creado.year)
                diagnostico["fecha"]=fecha
                query = db.GqlQuery("SELECT * FROM Diagnostico WHERE consulta = :1 ",consulta)
                diagnosticos=query.fetch(1)
                for eldiagnostico in diagnosticos:
                    diagnostico["diagnostico"]=eldiagnostico.nombre            
                lDiagonosticos.append(diagnostico)
        return lDiagonosticos