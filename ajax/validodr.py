import cgi
import wsgiref.handlers
import os
import datetime as dt
from google.appengine.ext import webapp, db
from modelos import Doctor,Usuario,Cita
from django.utils import simplejson
from templateCode.sesion import Sesion
from busquedausuario import BusquedaUsuario

class ValidoDoctor():
    def ExisteDr(self,Usuario):
	bRetorno=True
	if self.instanciaDoctor(Usuario) ==None:
	    bRetorno=False
	return bRetorno

    def instanciaDoctor(self,Usuario):
	busqueda=BusquedaUsuario()
        Usuario=str(Usuario).upper()
	instanciadr=None
	if busqueda.Busco(Usuario): #si existe el usuario
	    query = db.GqlQuery("SELECT * FROM Usuario WHERE usuario = :1 ",Usuario)
	    usuario = query.fetch(1)
	    query=None
	    for usr in usuario: #solo debe ser uno - ver fetch-
		query = db.GqlQuery("SELECT * FROM Doctor WHERE usuario = :1 ",usr)
	    dr = query.fetch(1)
	    for doctor in dr:
		instanciadr=doctor
		break
	return instanciadr
