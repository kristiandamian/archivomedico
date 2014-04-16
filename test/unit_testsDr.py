import unittest
import logging
import datetime as dt
from google.appengine.ext import db
from modelos import Doctor
from ajax.validodr import ValidoDoctor
from unit_tests import CreoUsuarios

class AltaPaciente(unittest.TestCase):

    def setUp(self):
        CreoUsuarios()
    
    def test_NoExistedr(self):        
        instdr=ValidoDoctor()
        doctor=instdr.instanciaDoctor("drInexistente".upper())
        self.assertEqual(doctor,None)
    
    def test_Existedr(self):        
        instdr=ValidoDoctor()
        doctor=instdr.instanciaDoctor("pruebadr".upper())
        self.assertNotEqual(doctor,None)
  

