import os
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from absolutePath import AbsolutePath
from modelos import Estudio
from decoratorlogin import RequierePermisosDoctoroSecretaria, RequierePermisosDoctoroPaciente
from ajax.grabopaciente import GraboPaciente
from ajax.validodr import ValidoDoctor
from ajax.validousuario import ValidoUsuario
from sesion import Sesion
from diagnosticos import Diagnosticos

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class RegistrarEstudios(webapp.RequestHandler):
    @RequierePermisosDoctoroSecretaria
    def get(self):
        MyPath=AbsolutePath()
        path=MyPath.getAbsolutePath()
        pathtemplate = os.path.join(path, 'templates/registrarEstudio.html')
        template_values ={
                            "upload_url": blobstore.create_upload_url('/upload'),
                        }
        sess = Sesion()
        self.response.out.write(template.render(pathtemplate, template_values))
    
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        estudio=Estudio ()
        estudio.nombre=self.request.get('nombreEstudio')
        estudio.archivo=blob_info.key()
        estudio.put()
        self.redirect('../verestudios' )  

class VerEstudios(webapp.RequestHandler):
    @RequierePermisosDoctoroPaciente
    def get(self):
        MyPath=AbsolutePath()
        path=MyPath.getAbsolutePath()
        pathtemplate = os.path.join(path, 'templates/verEstudios.html')
        sess = Sesion()
        diagnostico=Diagnosticos()
        template_values ={                                
                            'dr':diagnostico.EsDoctor(sess.getUser())
                        }
        self.response.out.write(template.render(pathtemplate, template_values))
