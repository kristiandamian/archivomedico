import unittest
import logging
import datetime as dt
from google.appengine.ext import db
from modelos import Doctor, Cita, Relacion
from ajax.grabocita import BuscoCita, GraboCita
from ajax.validodr import ValidoDoctor
from ajax.validousuario import ValidoUsuario
from templateCode.citas import Citas
from unit_tests import CreoUsuarios

class AltaPaciente(unittest.TestCase):

    def setUp(self):
        CreoUsuarios()
        self.CreoCita()
        self.CreoRelaciones()
    
    def test_NoExisteCita(self):
        cita=BuscoCita()
        #instdr=ValidoDoctor()
        #doctor=instdr.instanciaDoctor("pruebadr".upper())
        self.assertEqual(cita.BuscoCita("27-08-2009","10:00","10:30","pruebadr".upper()),0)
    
    def test_ExisteCita(self):
        cita=BuscoCita()
        #instdr=ValidoDoctor()
        #doctor=instdr.instanciaDoctor("pruebadr".upper())                
        self.assertNotEqual(cita.BuscoCita("27-08-2009","1:00","1:30","pruebadr".upper()),0,-1)
  
    def test_DoctoresRelacionadosConPaciente(self):
        cita=Citas()
        doctores=cita.ObtenerDoctores("prueba".upper())
        self.assertNotEqual(doctores,[])

    def test_DoctoresRelacionadosConDoctor(self):#devuelve a el mismo??
        cita=Citas()
        doctores=cita.ObtenerDoctores("pruebadr".upper())
        self.assertNotEqual(doctores,[])        

    def test_SIN_DoctoresRelacionadosConPaciente(self):
        cita=Citas()
        doctores=cita.ObtenerDoctores("UsuarioInexistente".upper())
        self.assertEqual(doctores,[])
  
    def test_AltaCita(self):
        grabocita=GraboCita()
        res=grabocita.AltaCita("pruebadr".upper(),"prueba".upper(),False,"prueba de paciente","12/03/80","7:00","7:30",1)
        cita=db.get(res)
        self.assertEqual(cita.doctor.usuario.usuario,"pruebadr".upper())
    
    def test_ObtengoCitas(self):
        cita=Citas()
        res=cita.Citas("pruebadr".upper(),"27/08/09")
        self.assertNotEqual(res,[])
        
    def CreoCita(self):
        instdr=ValidoDoctor()
        doctor=instdr.instanciaDoctor("pruebadr".upper())
        cita=Cita()
        cita.fecha="27/08/09"
        inicio="27/08/09 1:00"
        fin="27/08/09 1:30"
        cita.horaInicial=dt.datetime.strptime(inicio, "%d/%m/%y %H:%M")
        cita.horaFinal=dt.datetime.strptime(fin, "%d/%m/%y %H:%M")
        cita.duracion=30
        cita.doctor=doctor
        cita.pacientenuevo="miPacienteNuevo"
        cita.put()
    
    def CreoRelaciones(self):
        instancia=ValidoUsuario()
        instdr=ValidoDoctor()
        doctor=instdr.instanciaDoctor("pruebadr".upper())
        usuario=instancia.InstaciaUsuario("prueba".upper())
        relacion=Relacion()
        relacion.doctor=doctor
        relacion.usuario=usuario
        relacion.put()
    
