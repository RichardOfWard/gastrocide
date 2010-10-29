from OpenGL.GL import *
from OpenGL.GLU import *
import cPickle

class LookDownIsoCam:
	def __init__(self):
		self.zoom=10
	def setup(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		z=self.zoom
		glOrtho(-z,z,-z,z,-z,z)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(
				0,0,1, #eye
				0,0,0, #center
				0,1,0, #up
				)
	
class Triangle:
	def __init__(self):
		self.time=0.0
	def render(self):
		glRotate(self.time,0,0,1)
		glBegin(GL_QUADS)
		glVertex2d(0,0)
		glVertex2d(0,1)
		glVertex2d(1,0)
		glVertex2d(0,0)
		glEnd()
		self.time+=1

class MeshModel:
	def __init__(self,filename):
		f=file(filename,"rb")
		verts3=cPickle.load(f)
		verts3=cPickle.load(f)
