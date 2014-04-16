import os
import sha
import time
import Cookie

COOKIE_NAME = 'armedpay'

class SesionPayment(object):

    def load(self):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)
        value=1
        if self.cookie.get(COOKIE_NAME):
            value  = self.cookie[COOKIE_NAME].value            
        return value


    def store(self, cantidad, expire=7200):
        """Grabo la cookie que exipira por default en 2 horas"""
        self.cookie = Cookie.SimpleCookie()
        self.cookie[COOKIE_NAME] =cantidad
        self.cookie[COOKIE_NAME]['expires'] = expire
        self.cookie[COOKIE_NAME]['path'] = '/'
        print 'Set-Cookie: %s; HttpOnly' % (self.cookie.output().split(':', 1)[1].strip())


