from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

GAME_OBJ=None
def get_game():
	global GAME_OBJ
	if GAME_OBJ is not None:
		return GAME_OBJ

	from blib.mgr import MgrRender,MgrGame,MgrTeam
	class Game:
		def __init__(self):
			self.mgr_render=MgrRender()
			self.mgr_game=MgrGame()
			self.mgr_team=MgrTeam()
			self.keys={}

			self.keys["up"]=False
			self.keys["down"]=False
			self.keys["left"]=False
			self.keys["right"]=False
			self.keys[" "]=False
			self.keys["\r"]=False

			self.tower_height=3
			self.tower_section_height=10.0
			self.img=None
		def load(self):
			from blib.object import PlayerBlob, RingLevel, MeshModel, TowerSection, TowerSpire, Enemy1, Spawner,RingOuter

			self.rings=[]
			strength=6.0
			for i in range(self.tower_height):
				t=TowerSection()
				t.position[2]=self.tower_section_height/2+i*self.tower_section_height
				t.add_to_world()
				r=RingLevel(strength)
				ro=RingOuter()
				strength/=2
				r.position[2]=ro.position[2]=t.position[2]
				self.rings.append(r)
				r.add_to_world()
				ro.add_to_world()
			ts=TowerSpire()
			ts.position[2]=self.get_ring_height()
			ts.add_to_world()

			PlayerBlob().add_to_world()
			Spawner(Enemy1).add_to_world()
			self.set_img("assets/intro.bmp")
			self.restart=False
		def get_ring_height(self):
			if self.tower_height>0:
				return self.rings[self.tower_height-1].position[2]
			return 0.0
		
		def set_img(self,name):
			if name is None:
				if self.img is not None:
					glDeleteTextures(self.img)
				self.img=None
				return
			from PIL.Image import open
			im = open(name)
			try:
				ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
			except SystemError:
				ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
			ID = glGenTextures(1)
			glBindTexture(GL_TEXTURE_2D, ID)
			glPixelStorei(GL_UNPACK_ALIGNMENT,1)
			glTexImage2D(
					GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,
					GL_RGBA, GL_UNSIGNED_BYTE, image
					)
			self.img=ID
		def tick(self):
			if self.img is not None:
				if self.keys['\r']:
					self.set_img(None)
					if self.restart:
						self.__init__()
						self.load()
			if self.img is None:
				self.mgr_game.tick()
			self.mgr_render.render()
			if self.img is not None:
				glMatrixMode(GL_PROJECTION)
				glLoadIdentity()
				glOrtho(-1,1,-1,1,-1,1)
				glMatrixMode(GL_MODELVIEW)
				glLoadIdentity()
				gluLookAt(0,0,1,0,0,0,0,1,0)
				glEnable(GL_TEXTURE_2D)
				glDisable(GL_BLEND)
				glDisable(GL_LIGHTING)
				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
				glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
				glBindTexture(GL_TEXTURE_2D, self.img)
				glBegin(GL_QUADS)
				glTexCoord2f( 1.0,  1.0); glVertex3f( 1.0,  1.0, 1.0)
				glTexCoord2f( 1.0,  0.0); glVertex3f( 1.0, -1.0, 1.0)
				glTexCoord2f( 0.0,  0.0); glVertex3f(-1.0, -1.0, 1.0)
				glTexCoord2f( 0.0,  1.0); glVertex3f(-1.0,  1.0, 1.0)
				glEnd()
				glDisable(GL_TEXTURE_2D)
				glEnable(GL_BLEND)
				glEnable(GL_LIGHTING)
	GAME_OBJ=Game()
	return get_game()


