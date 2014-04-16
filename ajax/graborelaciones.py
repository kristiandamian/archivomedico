from modelos import Relacion, Doctor, Usuario
from validodr import ValidoDoctor
from validousuario import ValidoUsuario
from google.appengine.ext import  db

class GraboRelaciones():
    def Grabar(self,dr,usuario):
        usuario=str(usuario).upper()
        dr=str(dr).upper()
        instanciaDr=ValidoDoctor()
        doctor=instanciaDr.instanciaDoctor(dr)
        instanciaUsuario=ValidoUsuario()
        user=instanciaUsuario.InstaciaUsuario(usuario)
        bRetorno=True
        if user!=None and doctor!=None:
            if not self.ExisteRelacion(doctor,user):
                try:
                    relacion=Relacion()
                    relacion.doctor=doctor
                    relacion.usuario=user
                    relacion.put()
                except:
                    bRetorno=False
        else:
            bRetorno=False
        return bRetorno
    
    def ExisteRelacion(self,dr,usuario):
        """Compruebo si ya existe la relacion entre el dr y el usuario
            PARAMETROS:
            dr: instancia del modelo doctor
            usuario: instancia del modelo usuario (debe ser secretaria o paciente solamente)
            RETURN:
            False si no existe (que esto deberia pasar)
            TRUE si ya existe (no volver a grabar)
        """
        bRetorno=False
        query=db.GqlQuery("select * from Relacion where usuario=:1 and doctor=:2",usuario, dr)
        if query.count()>0:
            bRetorno=1
        else: #no existe, entonces valido que NO sea un dr
            instanciaDr=ValidoDoctor()
            if instanciaDr.ExisteDr(usuario.usuario):#es un Dr. no se puede grabar ese tipo de relaciones, es pecado
                bRetorno=True
        return bRetorno
        