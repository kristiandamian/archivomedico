import os

class AbsolutePath():
	def getAbsolutePath(self):
                """para poder usar subdirectorios, esto me pone al principio (raiz) del proyecto - NO MOVER ESTE ARCHIVO"""
                return os.path.dirname(__file__)


