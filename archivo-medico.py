import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app
import webapp2
from templateCode.datosDr import DatosDr
from templateCode.citas import Citas
from templateCode.consulta import Consulta
from templateCode.datosPaciente import DatosPaciente
from templateCode.datosSecretaria import DatosSecretaria
from templateCode.MainPage import MainPage
from templateCode.login import Login, Logout
from ajax.sign import signMobile
from movil.menumovil import menuMovil
from movil.errorMovil import errorMovil
from movil.busquedamovil import BusquedaMovil
from movil.historialmovil import HistorialMovil
from movil.logout import LogoutMovil
from ajax.validousuario import ValidoUsuario, ValidoUsuarioDr
from templateCode.cancelar import Cancelar
from ajax.busquedausuario import BusquedaUsuario
from ajax.altausuario import AltaUsuario
from ajax.grabopaciente import GraboPaciente#, GraboCookiePaciente
from ajax.grabosecretaria import GraboSecretaria
from ajax.grabodr import GraboDR
from ajax.grabocita import BuscoCita, GraboCita, ObtengoCitas, BorroCita
from ajax.buscopaciente import BuscoPaciente
from ajax.renovarsubscripcion import RenovarSubscripcion
from ajax.graboconsulta import GraboConsulta, GraboSintoma, GraboDiagnostico, GraboReceta
from templateCode.finalizarpago import FinalizarPago
from templateCode.subscribirse import Subscribirse
from templateCode.pago import Pago
from templateCode.diagnosticos import Diagnosticos
from templateCode.estudios import RegistrarEstudios, VerEstudios, UploadHandler

#Defino  la pantalla principal dentro de la clase MainPage
#Este objeto app manejara las peticiones
app = webapp2.WSGIApplication([
    ('/', Login),
    ('/datosdr',DatosDr),
    ('/datospaciente',DatosPaciente),
    ('/datossecretaria',DatosSecretaria),
    ('/citas',Citas), 
    ('/consulta',Consulta),    
    ('/validoPassword',ValidoUsuario),
    ('/validoPasswordDr',ValidoUsuarioDr),
    ('/logout',Logout),
    ('/finalizarpago/(.*)',FinalizarPago),
    ('/busquedausuario',BusquedaUsuario),
    ('/altausuario',AltaUsuario),
    ('/renovarsubscripcion',RenovarSubscripcion),
    ('/subscribirse',Subscribirse),
    ('/grabopaciente',GraboPaciente),
    ('/buscopaciente',BuscoPaciente),
    ('/grabosecretaria',GraboSecretaria),
    #('/graboCPaciente',GraboCookiePaciente),    
    ('/grabodr',GraboDR),
    ('/grabocita',GraboCita),
    ('/buscocita',BuscoCita),
    ('/diagnosticos',Diagnosticos),
    ('/verestudios',VerEstudios),
    ('/registrarestudios',RegistrarEstudios),
    ('/upload', UploadHandler),
    ('/obtengocitas/(.*)',ObtengoCitas),
    ('/graboconsulta/(.*)',GraboConsulta),
    ('/borrocita',BorroCita),
    ('/grabosintoma',GraboSintoma),
    ('/grabodiagnostico',GraboDiagnostico),
    ('/graboreceta',GraboReceta),    
    ('/pay',Pago),
    ('/cancelar',Cancelar),
    #movil!!!
    ('/buscarmovil',BusquedaMovil),
    ('/signmobile',signMobile),
    ('/menumovil',menuMovil),
    ('/errormovil',errorMovil),
    ('/hitorialmovil',HistorialMovil),
    ('/logoutmovil',LogoutMovil),
    ],debug=True)

		
#def main():
#    run_wsgi_app(application)

    
#si lo corro como funcion principal que hago? Creo una instancia de application
if __name__ == '__main__':
    main()
