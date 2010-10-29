import cPickle
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.vertex_buffer_object import *

from blib.game import get_game

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
	
class Visual:
	def add_to_world(self):
		get_game().mgr_render.add_object(self)
	def remove_from_world(self):
		get_game().mgr_render.remove_object(self)
	
class Triangle(Visual):
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

class MeshModel(Visual):
	def __init__(self,filename):
		f=file("assets/"+filename+".pkl","rb")
		self.v3=cPickle.load(f)
		self.v4=cPickle.load(f)
		self.v3=[float(v) for v in self.v3]
		self.i3=numpy.arange(len(self.v3)/3)
		self.i4=numpy.arange(len(self.v4)/4)
		self.v3=numpy.array(self.v3, 'f').reshape(-1,3)
		self.v4=numpy.array(self.v4, 'f').reshape(-1,3)
	def render(self):
		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointerf(self.v3)
		glDrawElementsui(GL_TRIANGLES, self.i3)
		glVertexPointerf(self.v4)
		glDrawElementsui(GL_QUADS, self.i4)

