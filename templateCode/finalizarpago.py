import cgi
import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from paypal.paypal import PayPal
from sesionPay import SesionPayment
from absolutePath import AbsolutePath
from sesion import Sesion

class FinalizarPago (webapp.RequestHandler):
	def get(self,req):
                MyPath=AbsolutePath()
		ABSpath=MyPath.getAbsolutePath()
##                try:
                paypal = PayPal()
                token=self.request.get('token')
                PayerID=self.request.get('PayerID')
                #obtengo la cantidad del cookie
                cookie=SesionPayment()
                cantidad=cookie.load()
                if int(cantidad)>0:
                        respuesta=paypal.DoExpressCheckoutPayment(token,PayerID,cantidad)
                        if self.find_key(respuesta,"ACK"):
                                if respuesta["ACK"]=='Success':
                                        self.session=Sesion()
                                        self.session.store(token,3600,'armedPS')#la sesion dura una hora en la cookie armedPS
                                        path = os.path.join(ABSpath, 'templates/finalizarpago.html')	
                                        self.response.out.write(template.render(path, None))
                                else:
                                        path = os.path.join(ABSpath, 'templates/cancelar.html')
                                        template_values={
                                                        'mensaje': 'La operaci&oacute;n fue cancelada por PayPal',
                                                }
                                        self.response.out.write(template.render(path, template_values))
                        else:
                                path = os.path.join(ABSpath, 'templates/cancelar.html')
                                template_values={
                                                'mensaje': 'La operaci&oacute;n fue cancelada, Respuesta incorrecta por parte de PayPal',
                                        }
                                self.response.out.write(template.render(path, template_values))
                else:
                        path = os.path.join(ABSpath, 'templates/cancelar.html')
                        template_values={
                                'mensaje': 'La operaci&oacute;n fue cancelada, Error en los cookies',
                        }
                        self.response.out.write(template.render(path, template_values))
##                except:
##                                path = os.path.join(ABSpath, 'templates/cancelar.html')
##                                template_values={
##                                                'mensaje': 'Ocurrio un error.<br> La operaci&oacute;n fue cancelada.',
##                                        }
##                                self.response.out.write(template.render(path, template_values))


        def find_key(self,dic, val):
            """Devuelve verdadero si existe la llave en el diccionario"""
            bRetorno=False
            for k in dic.iteritems():
                if k[0] == val:
                        bRetorno=True
                        break
            return bRetorno
                

