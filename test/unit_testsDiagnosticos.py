import unittest
import logging
import datetime as dt
from google.appengine.ext import db
from modelos import Usuario,Doctor,Paciente,Diagnostico, Consulta
from unit_tests import CreoUsuarios
from ajax.validodr import ValidoDoctor
from ajax.validousuario import ValidoUsuario
from templateCode.diagnosticos import Diagnosticos

class AltaDiagnosticos(unittest.TestCase):

    def setUp(self):
        CreoUsuarios()
        self.CreoConsulta()
    
    def test_NoExisteDiagnosticos(self):        
        inst=Diagnosticos()
        diag=inst.ObtengoDiagnosticos("UsuarioInexistente".upper())
        self.assertEqual(diag,[])
    
    def test_ExisteDiagnosticosPaciente(self):        
        inst=Diagnosticos()
        diag=inst.ObtengoDiagnosticos("prueba".upper())
        self.assertEqual(diag,False)

    def test_ExisteDiagnosticosDr(self):        
        inst=Diagnosticos()
        diag=inst.ObtengoDiagnosticos("testdr".upper())
        self.assertEqual(diag,[])

        
    def CreoConsulta(self):
        valuser=ValidoUsuario()
        valdr=ValidoDoctor()
        usuario=valuser.InstaciaUsuario("prueba".upper())
        dr=valdr.instanciaDoctor("pruebadr".upper())
        
        consulta=Consulta()
        consulta.doctor=dr
        consulta.usuario=usuario
        consulta.put()
        
        diagnostico=Diagnostico()
        diagnostico.consulta=consulta
        diagnostico.nombre="mi fabuloso diagnostico, bla, bla, bla, bla, bla."
        diagnostico.put()