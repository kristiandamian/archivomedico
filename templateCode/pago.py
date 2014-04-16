import cgi
import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from paypal.paypal import PayPal
from sesionPay import SesionPayment


class Pago (webapp.RequestHandler):
	def post(self):
		paypal = PayPal()
		cantidad=self.request.get('cantidad')
		#grabo en una cookie el valor a pagar
		cookie=SesionPayment()
		cookie.store(cantidad)

		pp_token = paypal.SetExpressCheckout(cantidad)
		express_token = paypal.GetExpressCheckoutDetails(pp_token)
		url= paypal.PAYPAL_URL + express_token
		self.redirect(url)


