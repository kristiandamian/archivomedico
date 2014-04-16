import unittest
import logging
from google.appengine.ext import db
from modelos import Usuario, Paciente, Doctor, Secretaria
from ajax.grabopaciente import GraboPaciente, GraboCookiePaciente

class AltaPaciente(unittest.TestCase):

    def setUp(self):
        CreoUsuarios()
        
    def tearDown(self):
        pass #no se necesita borrar las entidades de prueba

    
    def test_EsPaciente(self):
        paciente=GraboPaciente()        
        self.assertTrue(paciente.ExistePaciente("prueba".upper()))
        
    def test_NoEsPaciente(self):
        paciente=GraboPaciente()        
        self.assertFalse(paciente.ExistePaciente("pruebadr".upper()))
        
    def test_instanciaPacienteCuandoEsPaciente(self):
        paciente=GraboPaciente()
        self.assertNotEqual(paciente.instanciaPaciente("prueba".upper()),None)
    
    def test_instanciaPacienteCuandoEsDr(self):
        paciente=GraboPaciente()
        self.assertEqual(paciente.instanciaPaciente("pruebadr".upper()),None)


class ProbarGrabarCookie(unittest.TestCase):
    def setUp(self):
        CreoUsuarios() 
        
    def test_PruebaCookiesCuandoEsPaciente(self):
        cookie=GraboCookiePaciente()
        key=cookie.instanciaPaciente("prueba".upper())
        self.assertNotEqual(key,0)
        
    def test_PruebaCookiesCuandoEsDr(self):
        cookie=GraboCookiePaciente()
        key=cookie.instanciaPaciente("pruebadr".upper())
        self.assertEqual(key,0)
   

def CreoUsuarios():
    """Creo un usuario Paciente -prueba- y uno Dr. -pruebadr- para lo que se ofrezca"""
    #alta paciente
    usuario=Usuario()
    usuario.usuario="prueba".upper()
    usuario.password="123"
    usuario.correo="kristiandamian@gmail.com"
    usuario.put()
    paciente=Paciente()
    paciente.usuario=usuario
    paciente.nombre="paciente"
    paciente.paterno="PacientePaterno"
    paciente.materno="MaternoPaciente"
    paciente.fecha_nacimiento="12/03/1980"
    paciente.estatura=1.72
    paciente.peso=float(82)
    paciente.correo="dcastrok@homex.com.mx"
    paciente.put()
    
    #alta doctor
    usuario=Usuario()
    usuario.usuario="pruebadr".upper()
    usuario.password="123"
    usuario.correo="kristiandamian@gmail.com"
    usuario.put()
    doctor=Doctor()
    doctor.usuario=usuario
    doctor.nombre="dr"
    doctor.paterno="drPaterno"
    doctor.materno="drPaciente"
    doctor.fecha_nacimiento="12/03/1980"
    doctor.estatura=1.72
    doctor.peso=float(82)
    doctor.correo="dcastrok@homex.com.mx"
    doctor.put()
    
    #alta secretaria
    usuario=Usuario()
    usuario.usuario="secretaria".upper()
    usuario.password="123"
    usuario.correo="kristiandamian@gmail.com"
    usuario.put()
    secretaria=Secretaria()
    secretaria.usuario=usuario
    secretaria.nombre="secretaria"
    secretaria.paterno="perez"
    secretaria.materno="de la o"
    secretaria.telefono="7507070"
    secretaria.celular="6679949494"
    secretaria.direccion="la calle street #461 col. buenavista"
    secretaria.put()
    return False