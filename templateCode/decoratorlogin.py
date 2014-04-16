#from appEngineUtilities.sessions import Session
from sesion import Sesion
from django.http import HttpResponsePermanentRedirect
from ajax.validodr import ValidoDoctor
from ajax.grabosecretaria import GraboSecretaria
from ajax.grabopaciente import GraboPaciente

def loginRequerido(func):
        """Decorador para que si no tiene una sesion activa se vaya a la pantalla de login"""
        def redirigir(self,*args, **kw):                
        	sess = Sesion()
        	if sess.load():
                        return func(self, *args, **kw)
                else:
			Mensaje("Login requerido")
			#print'Content-Type: text/html'
			#print '<h1>Login requerido</h1>'
			#print '<script type="text/javascript">'
			#print '<!--'
			#print 'window.location = "/"'
			#print '//-->'
			#print '</script>'			
        return redirigir
        
def RequierePermisosDoctor(func):
	def redirigir(self,*args,**kw):
		sess = Sesion()
		if sess.load():
			validodr=ValidoDoctor()
			if validodr.ExisteDr(sess.getUser()):
				return func(self, *args, **kw)
			else:
				Mensaje("No tiene los permisos necesarios")
	return redirigir

def RequierePermisosSecretaria(func):
	def redirigir(self,*args,**kw):
		sess = Sesion()
		if sess.load():
			validosecre=GraboSecretaria()			
			if validosecre.ExisteSecretaria(sess.getUser()):
				return func(self, *args, **kw)
			else:
				Mensaje("No tiene los permisos necesarios")
	return redirigir

def RequierePermisosDoctoroSecretaria(func):
	def redirigir(self,*args,**kw):
		sess = Sesion()
		if sess.load():
			validosecre=GraboSecretaria()
			validodr=ValidoDoctor()
			if validosecre.ExisteSecretaria(sess.getUser()) or validodr.ExisteDr(sess.getUser()):
				return func(self, *args, **kw)
			else:
				Mensaje("No tiene los permisos necesarios")
	return redirigir

def RequierePermisosDoctoroPaciente(func):
	def redirigir(self,*args,**kw):
		sess = Sesion()
		if sess.load():
			validopaciente=GraboPaciente()
			validodr=ValidoDoctor()
			if validopaciente.ExistePaciente(sess.getUser()) or validodr.ExisteDr(sess.getUser()):
				return func(self, *args, **kw)
			else:
				Mensaje("No tiene los permisos necesarios")
	return redirigir

def Mensaje(texto):
	print 'Content-Type: text/html '
	print '<h1>'+texto+'</h1>'
	print '<script type="text/javascript">'
        print '<!--'
        print 'window.location = "/"'
        print '//-->'
        print '</script>'
	