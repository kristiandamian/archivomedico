import os
import sha
import time
import Cookie
from key import secretKey

COOKIE_NAME = 'armed'

class Sesion(object):

    def __init__(self):
        self.time  = None
        self.user  = None
        self.auth  = None
        self.seed  = secretKey()

    def load(self,COOKIE_NAME_2=COOKIE_NAME):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)
        if self.cookie.get(COOKIE_NAME_2):
            value  = self.cookie[COOKIE_NAME_2].value
            tokens = value.split(':')
            if len(tokens) != 3:
                return False
            else:
                h = tokens[2]
                tokens = tokens[:-1]
                tokens.append(self.seed)
                if h == self.hash(tokens):
                    self.time = tokens[0]
                    self.user = tokens[1]
                    self.auth = h
                    try:
                        t = int(self.time)
                    except:
                        return False
                    if t > int(time.time()):
                        return True
        return False

    def getUser(self,COOKIE_NAME_2=COOKIE_NAME):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)
        if self.cookie.get(COOKIE_NAME_2):
            value  = self.cookie[COOKIE_NAME_2].value
            tokens = value.split(':')
            if len(tokens) != 3:
                return False
            else:
                return tokens[1] #devuelvo el nombre del usuario - 2da posicion

    def store(self, user, expire=28800,COOKIE_NAME_2=COOKIE_NAME):
        """Grabo la cookie que exipira por default en 8 horas"""
        self.time = str(int(time.time())+expire)
        self.user = user
        params = [self.time, self.user, self.seed]
        self.auth = self.hash(params)
        params = [self.time, self.user, self.auth]
        self.cookie = Cookie.SimpleCookie()
        self.cookie[COOKIE_NAME_2] = ':'.join(params)
        self.cookie[COOKIE_NAME_2]['expires'] = expire
        self.cookie[COOKIE_NAME_2]['path'] = '/'
        print 'Set-Cookie: %s; HttpOnly' % (self.cookie.output().split(':', 1)[1].strip())

    def hash(self, params):
        return sha.new(';'.join(params)).hexdigest()

    def logout(self,COOKIE_NAME_2=COOKIE_NAME):
        self.store('', 0,COOKIE_NAME_2)
