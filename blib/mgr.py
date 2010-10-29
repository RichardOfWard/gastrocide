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
			self.cam.setup()
		for ob in self.vis_obs:
			glPushMatrix()
			ob.render()
			glPopMatrix()


