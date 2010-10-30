import cPickle
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.vertex_buffer_object import *

from blib.game import get_game
from blib.colors import *

class MeshAssets:
	def __init__(self,filename):
		f=file("assets/"+filename+".pkl","rb")
		self.store=store=cPickle.load(f)
		for k in store.keys():
			v3,n3,v4,n4=store[k]
			i3=numpy.arange(len(v3)/3)
			i4=numpy.arange(len(v4)/3)
			v3=numpy.array(v3, 'f').reshape(-1,3)
			v4=numpy.array(v4, 'f').reshape(-1,3)
			n3=numpy.array(n3, 'f').reshape(-1,3)
			n4=numpy.array(n4, 'f').reshape(-1,3)
			store[k]=(v3,n3,i3,v4,n4,i4)
	def get(self,name):
		return self.store[name]
MeshAssets=MeshAssets("blob")

class LookDownIsoCam:
	def __init__(self):
		self.zoom=10
	def setup_proj(self):
		z=self.zoom
		w=float(glutGet(GLUT_WINDOW_WIDTH))
		h=float(glutGet(GLUT_WINDOW_HEIGHT))
		if h>w:
			h=(h/w)*z
			w=z
		else:
			w=(w/h)*z
			h=z
		w/=2.0
		h/=2.0
		z/=2.0

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-w,w,-h,h,-z,z)

	def setup_model(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(
				0.0,1.0,0.0, #eye
				0.0,0.0,0.0, #center
				0.0,0.0,1.0, #up
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
		self.time+=1
		glBegin(GL_QUADS)
		glVertex2d(0,0)
		glVertex2d(0,1)
		glVertex2d(1,0)
		glVertex2d(0,0)
		glEnd()

class MeshModel(Visual):
	def __init__(self,name):
		self.v3,self.n3,self.i3,self.v4,self.n4,self.i4=MeshAssets.get(name)
		self.col_amb=white
		self.col_diff=white
		self.col_spec=white
	def render(self):
		glMaterialfv(GL_FRONT, GL_AMBIENT, self.col_amb)
		glMaterialfv(GL_FRONT, GL_DIFFUSE, self.col_diff)
		glMaterialfv(GL_FRONT, GL_SPECULAR, self.col_spec)
		glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_NORMAL_ARRAY)
		glVertexPointerf(self.v3)
		glNormalPointer(GL_FLOAT,0,self.n3)
		glDrawElementsui(GL_TRIANGLES, self.i3)
		glVertexPointerf(self.v4)
		glNormalPointer(GL_FLOAT,0,self.n4)
		glDrawElementsui(GL_QUADS, self.i4)

class Blob(MeshModel):
	def __init__(self,size,color=red):
		size=float(size)
		MeshModel.__init__(self,"blob")
		self.size=size
		self.col_amb=self.col_diff=color
	def render(self):
		MeshModel.render(self)

