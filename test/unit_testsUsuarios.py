import unittest
import logging
from google.appengine.ext import db
from modelos import Usuario, Paciente, Doctor
from ajax.busquedausuario import BusquedaUsuario
from ajax.validousuario import ValidoUsuario
from unit_tests import CreoUsuarios

class Usuarios(unittest.TestCase):

    def setUp(self):
        CreoUsuarios()
        
    def tearDown(self):
        pass #no se necesita borrar las entidades de prueba

    def test_ExisteUsuario(self):
        busqueda=BusquedaUsuario()  
        self.assertNotEqual(busqueda.Busco("prueba".upper()),0)
        
    def test_NOExisteUsuario(self):
        busqueda=BusquedaUsuario()  
        self.assertEqual(busqueda.Busco("UsuarioInexistente".upper()),0)
    
    def test_ExisteInstanciaUsuario(self):
        usuario=ValidoUsuario()
        usuarioinstanciado=usuario.InstaciaUsuario("prueba".upper())
        self.assertNotEqual(usuarioinstanciado,None)

    def test_NOExisteInstanciaUsuario(self):
        usuario=ValidoUsuario()
        usuarioinstanciado=usuario.InstaciaUsuario("UsuarioInexistente".upper())
        self.assertEqual(usuarioinstanciado,None)

        
