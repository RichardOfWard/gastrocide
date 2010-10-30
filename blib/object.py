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
		self.zoom=10.0
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
				0.0,4.0,1.0, #eye
				0.0,0.0,0.0, #center
				0.0,0.0,1.0, #up
				)
class Cam:
	def __init__(self,fov=60.0,ob=None,position=(0.0,-5.0,1.0),offset=(0.0,0.0,1.0)):
		self.position=list(position)
		self.offset=list(offset)
		self.target=[0,0,0]
		self.fov=fov
		self.ob=ob
	def setup_proj(self):
		w=float(glutGet(GLUT_WINDOW_WIDTH))
		h=float(glutGet(GLUT_WINDOW_HEIGHT))
		aspect=w/h
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(self.fov,aspect,0.01,50)
	def setup_model(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		eye=self.position
		center=self.target
		if self.ob is not None:
			center=[self.ob.position[i]+self.offset[i] for i in range(3)]
			eye=[center[i]+self.position[i] for i in range(3)]
		up=[0.0,0.0,1.0]
		args=eye+center+up
		gluLookAt(*args)
	
class Visual:
	def __init__(self):
		self.transparent=False
	def add_to_world(self):
		get_game().mgr_render.add_object(self,self.transparent)
	def remove_from_world(self):
		get_game().mgr_render.remove_object(self)
	
class MeshModel(Visual):
	def __init__(self,name):
		Visual.__init__(self)
		self.v3,self.n3,self.i3,self.v4,self.n4,self.i4=MeshAssets.get(name)
		self.col_amb=white
		self.col_diff=white
		self.col_spec=white
		self.position=[0.0,0.0,0.0]
		self.zrot=0.0
		self.xrot=0.0
	def trans(self):
		glTranslate(*self.position)
		glRotate(self.zrot,0.0,0.0,-1.0)
		glRotate(self.xrot,-1.0,0.0,0.0)
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

class Tower(MeshModel):
	def __init__(self):
		MeshModel.__init__(self,"tower")
		col=list(darkslategray)
		self.col_amb=self.col_diff=col

class RingLevel(MeshModel):
	def __init__(self):
		MeshModel.__init__(self,"ring")
		col=list(slateblue)
		col[3]=0.8
		self.transparent=True
		self.col_amb=self.col_diff=col

class Blob(MeshModel):
	def __init__(self,size,color=red):
		size=float(size)
		MeshModel.__init__(self,"blob")
		self.size=size
		self.col_amb=self.col_diff=color
	def render(self):
		MeshModel.render(self)

class PlayerBlob(Blob):
	def __init__(self):
		Blob.__init__(self,1,green)
		self.cam=None
		self.position[1]=-5.0
		self.position[2]=0.5
		self.zrot=90
	def add_to_world(self):
		Visual.add_to_world(self)
		cam=self.cam=Cam(ob=self)
		get_game().mgr_render.cam=cam
		get_game().mgr_game.add_object(self)
	def tick(self):
		pass
		
