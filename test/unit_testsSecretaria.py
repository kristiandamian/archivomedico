import unittest
import logging
import datetime as dt
from google.appengine.ext import db
from modelos import Secretaria
from ajax.grabosecretaria import GraboSecretaria
from unit_tests import CreoUsuarios

class AltaPaciente(unittest.TestCase):

    def setUp(self):
        CreoUsuarios()
    
    def test_NoExisteSecretaria(self):        
        inst=GraboSecretaria()
        secretaria=inst.ExisteSecretaria("SecretariaInexistente".upper())
        self.assertEqual(secretaria,False)
    
    def test_ExisteSecretaria(self):        
        inst=GraboSecretaria()
        secretaria=inst.ExisteSecretaria("secretaria".upper())
        self.assertEqual(secretaria,True)
    
    def test_InstanciaValidaSecretaria(self):
        inst=GraboSecretaria()
        secretaria=inst.instanciaSecretaria("secretaria".upper())
        self.assertNotEqual(secretaria,None)
  

