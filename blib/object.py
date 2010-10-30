import cPickle
import numpy
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.arrays import vbo

from math import radians

from gob.vector3 import Vector3
from gob.matrix44 import Matrix44

from blib.game import get_game
from blib.colors import *

GRAVITY=0.03

class MeshAssets(object):
	def __init__(self,filename):
		f=file("assets/"+filename+".pkl","rb")
		self.store=store=cPickle.load(f)
		for k in store.keys():
			v3,n3,v4,n4=store[k]
			i3=len(v3)/3
			i4=len(v4)/3
			v3=numpy.array(v3, 'f').reshape(-1,3)
			v4=numpy.array(v4, 'f').reshape(-1,3)
			n3=numpy.array(n3, 'f').reshape(-1,3)
			n4=numpy.array(n4, 'f').reshape(-1,3)
			v3=vbo.VBO(v3)
			v4=vbo.VBO(v4)
			n3=vbo.VBO(n3)
			n4=vbo.VBO(n4)
			store[k]=(v3,n3,i3,v4,n4,i4)
	def get(self,name):
		return self.store[name]
MeshAssets=MeshAssets("blob")

class LookDownIsoCam(object):
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
class Cam(object):
	def __init__(self,fov=40.0,ob=None,position=(0.0,-8.0,1.0),offset=(0.0,0.0,1.0)):
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
		gluPerspective(self.fov,aspect,0.01,150)
	def setup_model(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		eye=self.position
		center=self.target
		if self.ob is not None:
			center=[self.ob.position[i]+self.offset[i] for i in range(3)]
			center[2]=get_game().get_ring_height()+2.5
			eye=[center[i]+self.position[i] for i in range(3)]
		up=[0.0,0.0,1.0]
		args=eye+center+up
		gluLookAt(*args)
	
class Visual(object):
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

		self.v3.bind()
		glVertexPointerf(self.v3)
		self.v3.unbind()
		self.n3.bind()
		glNormalPointerf(self.n3)
		glDrawArrays(GL_TRIANGLES, 0, self.i3)
		self.n3.unbind()


		self.v4.bind()
		glVertexPointerf(self.v4)
		self.v4.unbind()
		self.n4.bind()
		glNormalPointerf(self.n3)
		glDrawArrays(GL_QUADS, 0, self.i4)
		self.n4.unbind()

		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_NORMAL_ARRAY)


class TowerSection(MeshModel):
	def __init__(self):
		MeshModel.__init__(self,"tower_section")
		col=list(darkslategray)
		self.col_amb=self.col_diff=col

class TowerSpire(MeshModel):
	def __init__(self):
		MeshModel.__init__(self,"tower_spire")
		col=list(darkslategray)
		self.col_amb=self.col_diff=col

class RingLevel(MeshModel):
	def __init__(self,strength):
		MeshModel.__init__(self,"ring")
		col=list(slateblue)
		col[3]=0.8
		self.transparent=True
		self.col_amb=self.col_diff=col
		self.strength=strength
	def render(self):
		if self.strength-PLAYER.size<=self.strength/4.0:
			if random.randint(1,5)!=1:
				MeshModel.render(self)
		else:
			MeshModel.render(self)


class BlobBehaviourPlayerOnRing(object):
	def __init__(self,blob):
		self.blob=blob
		self.__speed=1.0
		self.was_moving_right=True
		self.mrm=Matrix44.z_rotation(radians( self.__speed))
		self.mlm=Matrix44.z_rotation(radians(-self.__speed))
		self.swapm=Matrix44.z_rotation(radians(180))

		self.vel=0.0

		self.on_floor=False

		self.bob=0.0
		self.bob_dir=1.0
		self.bob_mtx=numpy.array([
				1.0,0.0,0.0,0.0,
				0.0,1.0,0.0,0.0,
				0.0,0.0,1.0,0.0,
				0.0,0.0,0.0,1.0,
				])
	def move_left(self):
		b=self.blob
		b.position=list(self.mlm.transform(b.position))
		b.zrot+=self.__speed
		if self.was_moving_right:
			b.zrot+=180.0
		self.was_moving_right=False
		if b.zrot>360.0:
			b.zrot-=360.0
		self.step_bob()
	def move_right(self):
		b=self.blob
		b.position=list(self.mrm.transform(b.position))
		b.zrot-=self.__speed
		if not self.was_moving_right:
			b.zrot-=180.0
		self.was_moving_right=True
		if b.zrot<0.0:
			b.zrot+=360.0
		self.step_bob()
	def stop_movement(self):
		self.bob=0
		self.bob_dir=1.0
	def step_bob(self):
		self.bob+=self.bob_dir*0.07
		if self.bob_dir>0:
			if self.bob>1.0:
				self.bob=1.0
				self.bob_dir=-1.0
		else:
			if self.bob<0.0:
				self.bob=0.0
				self.bob_dir=1.0
	def jump(self):
		if self.on_floor:
			self.vel=0.5
	def tick(self):
		self.bob_mtx[9]=self.bob*0.6
		self.vel-=GRAVITY
		self.blob.position[2]+=self.vel
		self.on_floor=False
		rh=get_game().get_ring_height()+self.blob.size/2.0
		if rh>self.blob.position[2]:
			self.blob.position[2]=rh
			self.vel=0
			self.on_floor=True
		#apply damage
		enemies=list(get_game().mgr_team.obs[(self.blob.team+1)%2])
		me=Vector3(self.blob.position)
		for enemy in enemies:
			if self.vel<0.0 and not self.on_floor and not enemy.dead:
				them=Vector3(enemy.position)
				dist=(me-them).get_length()
				if 2*dist<self.blob.size+enemy.size:
					self.blob.position[2]-=self.vel
					enemy.damage()
					self.on_floor=True
					self.jump()
					self.on_floor=False
					break
			elif self.on_floor and enemy.dead:
				them=Vector3(enemy.position)
				dist=(me-them).get_length()
				if 2*dist<self.blob.size+enemy.size:
					self.blob.position[2]-=self.vel
					enemy.remove_from_world()
					self.blob.size+=0.1
					game=get_game()
					if self.blob.size>game.rings[game.tower_height-1].strength:
						game.tower_height-=1
				
			

class Blob(MeshModel):
	def __init__(self,size,color=red):
		size=float(size)
		MeshModel.__init__(self,"blob")
		self.size=size
		self.original_size=self.size
		self.col_amb=self.col_diff=color
		self.team=0
		self.dead=False
	def damage(self):
		self.size-=0.1
		for i in range(4):
			Damage(self).add_to_world()
		if self.size<=0.6*self.original_size and self.team==1:
			self.dead=True
			self.xrot=-90.0
			self.col_amb=[c*0.5 for c in self.col_amb]
			self.col_diff=[c*0.5 for c in self.col_diff]
			self.col_spec=[c*0.5 for c in self.col_spec]
			self.col_amb [3]=1.0
			self.col_diff[3]=1.0
			self.col_spec[3]=1.0
	def trans(self):
		super(Blob,self).trans()
		glScale(self.size,self.size,self.size)

PLAYER=None
class PlayerBlob(Blob):
	def __init__(self):
		global PLAYER
		PLAYER=self
		Blob.__init__(self,1,green)
		self.cam=None
		self.position[1]=-5.0
		self.position[2]=0.5+get_game().get_ring_height()+30.0
		self.zrot=90.0
		self.team=0
		self.behaviour=BlobBehaviourPlayerOnRing(self)
		self.dead=False
	def add_to_world(self):
		Visual.add_to_world(self)
		cam=self.cam=Cam(ob=self)
		get_game().mgr_render.cam=cam
		get_game().mgr_game.add_object(self)
		get_game().mgr_team.add_object(self,self.team)
	def remove_from_world(self):
		Visual.remove_from_world(self)
		get_game().mgr_game.remove_object(self)
		get_game().mgr_team.remove_object(self,self.team)
	def trans(self):
		super(PlayerBlob,self).trans()
		glMultMatrixf(self.behaviour.bob_mtx)
	def tick(self):
		if get_game().keys["left"]:
			self.behaviour.move_left()
		elif get_game().keys["right"]:
			self.behaviour.move_right()
		else:
			self.behaviour.stop_movement()
		if get_game().keys[" "]:
			self.behaviour.jump()
		self.behaviour.tick()

class Enemy(Blob):
	def __init__(self,size,color=red):
		Blob.__init__(self,size,red)
		self.position[1]=-5.0
		self.position[2]=0.5+get_game().get_ring_height()+30.0
		self.zrot=90.0
		self.team=1
		self.behaviour=BlobBehaviourPlayerOnRing(self)
		self.dead=False
	def trans(self):
		super(Enemy,self).trans()
		glMultMatrixf(self.behaviour.bob_mtx)
	def tick(self):
		self.behaviour.tick()
	def add_to_world(self):
		Visual.add_to_world(self)
		get_game().mgr_game.add_object(self)
		get_game().mgr_team.add_object(self,self.team)
	def remove_from_world(self):
		Visual.remove_from_world(self)
		get_game().mgr_game.remove_object(self)
		get_game().mgr_team.remove_object(self,self.team)

class Damage(MeshModel):
	def __init__(self,source):
		MeshModel.__init__(self,"damage")
		self.col_amb=source.col_amb
		self.col_diff=source.col_diff
		self.col_spec=source.col_spec
		self.position=source.position[:]
		self.vel=[
				(random.randint(0,100)-50)/500.0,
				(random.randint(0,100)-50)/500.0,
				0.25
		]
	def tick(self):
		self.vel[2]-=GRAVITY
		for i in range(3):
			self.position[i]+=self.vel[i]
		if self.position[2]<-10.0:
			self.remove_from_world()
	def add_to_world(self):
		Visual.add_to_world(self)
		get_game().mgr_game.add_object(self)
	def remove_from_world(self):
		Visual.remove_from_world(self)
		get_game().mgr_game.remove_object(self)

class Spawner():
	def __init__(self,klass,size,timeout=200):
		self.klass=klass
		self.size=size
		self.timeout=timeout
		self.timer=20
	def add_to_world(self):
		get_game().mgr_game.add_object(self)
	def tick(self):
		self.timer-=1
		if self.timer<=0:
			if len(get_game().mgr_team.obs[1])>=4:
				self.timer+=random.randint(1,20)
			else:
				self.timer=self.timeout
				inst=self.klass(size=self.size)
				m=Matrix44.z_rotation(radians(random.randint(1,360)))
				v=Vector3(inst.position)
				inst.position=list(m.transform(v))
				#player=list(get_game().mgr_team.obs[0])
				#if player:
				#	player=player[0]
				#	inst.position=player.position[:]
				#	inst.position[2]+=10.0
				inst.add_to_world()


