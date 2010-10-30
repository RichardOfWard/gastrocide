from blib.object import LookDownIsoCam
from OpenGL.GL import *
from OpenGL.GLU import *

class MgrRender:
	def __init__(self):
		self.vis_obs=set()
		self.cam=LookDownIsoCam()
	def add_object(self,ob):
		self.vis_obs.add(ob)
	def remove_object():
		self.vis_obs.remove(ob)
	def set_cam(self,cam):
		self.cam=cam
	def render(self):
		if self.cam is not None:
			self.cam.setup_proj()

		glEnable(GL_LIGHT0)
		glLight(GL_LIGHT0,GL_POSITION,[1.0,1.0,1.0,0])
		glLight(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
		glLight(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])

		if self.cam is not None:
			self.cam.setup_model()
		for ob in self.vis_obs:
			glPushMatrix()
			ob.render()
			glPopMatrix()


