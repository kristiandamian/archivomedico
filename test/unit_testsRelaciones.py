import unittest
import logging
import datetime as dt
from google.appengine.ext import db
from modelos import Relacion, Doctor, Usuario, Secretaria, Paciente
from ajax.graborelaciones import GraboRelaciones
from ajax.validodr import ValidoDoctor
from ajax.validousuario import ValidoUsuario
from unit_tests import CreoUsuarios

class AltaPaciente(unittest.TestCase):

    def setUp(self):
        CreoUsuarios()
        CreoRelaciones()
    
    def test_NoExisteRelacion(self):        
        inst=GraboRelaciones()
        instanciaDr=ValidoDoctor()
        doctor=instanciaDr.instanciaDoctor("pruebadr".upper())
        instanciaUsuario=ValidoUsuario()
        user=instanciaUsuario.InstaciaUsuario("secretaria".upper())        
        relacion=inst.ExisteRelacion(doctor,user)
        self.assertEqual(relacion,False)

    def test_NoExisteRelacionPorSerDr(self):        
        inst=GraboRelaciones()
        instanciaDr=ValidoDoctor()
        doctor=instanciaDr.instanciaDoctor("pruebadr".upper())
        instanciaUsuario=ValidoUsuario()
        user=instanciaUsuario.InstaciaUsuario("pruebadr".upper())

        relacion=inst.ExisteRelacion(doctor,user)
        self.assertEqual(relacion,True)        
    
    def test_ExisteRelacion(self):        
        inst=GraboRelaciones()
        instanciaDr=ValidoDoctor()
        doctor=instanciaDr.instanciaDoctor("pruebadr".upper())
        instanciaUsuario=ValidoUsuario()
        user=instanciaUsuario.InstaciaUsuario("prueba".upper())

        relacion=inst.ExisteRelacion(doctor,user)
        self.assertEqual(relacion,True)
    
    def test_GraboRelacion(self):
        usuario=Usuario()
        usuario.usuario="secretaria2".upper()
        usuario.password="123"
        usuario.correo="kristiandamian@gmail.com"
        usuario.put()
        secretaria=Secretaria()
        secretaria.usuario=usuario
        secretaria.nombre="secretaria2"
        secretaria.paterno="perez"
        secretaria.materno="de la o"
        secretaria.telefono="7507070"
        secretaria.celular="6679949494"
        secretaria.direccion="la calle street #461 col. buenavista"
        secretaria.put()
        inst=GraboRelaciones()
        relacion=inst.Grabar("pruebadr".upper(),"secretaria2".upper())
        self.assertEqual(relacion,True)

    def test_GraboRelacionFormaSecretaria(self):
        usuario=Usuario()
        usuario.usuario="secretaria2".upper()
        usuario.password="123"
        usuario.correo="kristiandamian@gmail.com"
        usuario.put()
        secretaria=Secretaria()
        secretaria.usuario=usuario
        secretaria.nombre="secretaria2"
        secretaria.paterno="perez"
        secretaria.materno="de la o"
        secretaria.telefono="7507070"
        secretaria.celular="6679949494"
        secretaria.direccion="la calle street #461 col. buenavista"
        secretaria.put()
        from ajax.grabosecretaria import GraboSecretaria
        grabsec=GraboSecretaria()
        grabsec.AltaRelaciones("pruebadr|".upper(),"secretaria2".upper())
        inst=GraboRelaciones()
        instanciaDr=ValidoDoctor()
        doctor=instanciaDr.instanciaDoctor("pruebadr".upper())
        relacion=inst.ExisteRelacion(doctor,usuario)
        self.assertEqual(relacion,True)        
        
    def test_NOGraboRelacion(self):
        inst=GraboRelaciones()
        relacion=inst.Grabar("pruebadr".upper(),"secretariaInexistente".upper())
        self.assertEqual(relacion,False)

def CreoRelaciones():
    instanciaDr=ValidoDoctor()
    doctor=instanciaDr.instanciaDoctor("pruebadr".upper())
    instanciaUsuario=ValidoUsuario()
    user=instanciaUsuario.InstaciaUsuario("prueba".upper())
    relacion=Relacion()
    relacion.usuario=user
    relacion.doctor=doctor
    relacion.put()
