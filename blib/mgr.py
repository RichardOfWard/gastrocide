from blib.object import LookDownIsoCam
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class MgrRender:
	def __init__(self):
		self.vis_obs=set()
		self.trans_obs=set()
		self.none_cam=LookDownIsoCam()
		self.cam=None
	def add_object(self,ob,transparent):
		if transparent:
			self.trans_obs.add(ob)
		else:
			self.vis_obs.add(ob)
	def remove_object(self,ob):
		if ob in self.vis_obs:
			self.vis_obs.remove(ob)
		if ob in self.trans_obs:
			self.trans_obs.remove(ob)
	def set_cam(self,cam):
		self.cam=cam
	def render(self):
		cam=self.cam
		if cam is None:
			cam=self.none_cam

		cam.setup_proj()


		glEnable(GL_LIGHT0)
		glLight(GL_LIGHT0,GL_POSITION,[1.0,-1.0,1.0,0])
		glLight(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
		glLight(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])


		cam.setup_model()
		for obs in (self.vis_obs,self.trans_obs):
			for ob in list(obs):
				glPushMatrix()
				ob.trans()
				ob.render()
				glPopMatrix()

class MgrGame():
	def __init__(self):
		self.tick_obs=set()
	def add_object(self,ob):
		self.tick_obs.add(ob)
	def remove_object(self,ob):
		if ob in self.tick_obs:
			self.tick_obs.remove(ob)
	def tick(self):
		for ob in list(self.tick_obs):
			ob.tick()
class MgrTeam():
	def __init__(self):
		self.obs=[set(),set()]
	def add_object(self,ob,team):
		self.obs[team].add(ob)
	def remove_object(self,ob,team):
		if ob in self.obs[team]:
			self.obs[team].remove(ob)

