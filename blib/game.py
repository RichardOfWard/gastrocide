GAME_OBJ=None
def get_game():
	global GAME_OBJ
	if GAME_OBJ is not None:
		return GAME_OBJ

	from blib.mgr import MgrRender,MgrGame
	class Game:
		def __init__(self):
			self.mgr_render=MgrRender()
			self.mgr_game=MgrGame()
			self.keys={}

			self.keys["up"]=False
			self.keys["down"]=False
			self.keys["left"]=False
			self.keys["right"]=False
			self.keys[" "]=False

			self.tower_height=5
			self.tower_section_height=10.0
		def load(self):
			from blib.object import PlayerBlob, RingLevel, MeshModel, TowerSection, TowerSpire

			self.rings=[]
			for i in range(self.tower_height):
				t=TowerSection()
				t.position[2]=self.tower_section_height/2+i*self.tower_section_height
				t.add_to_world()
				r=RingLevel()
				r.position[2]=t.position[2]
				self.rings.append(r)
				r.add_to_world()
			ts=TowerSpire()
			ts.position[2]=self.get_ring_height()
			ts.add_to_world()

			p=PlayerBlob()
			p.add_to_world()
			#for i in range(100):
			#	p=PlayerBlob()
			#	p.add_to_world()
		def get_ring_height(self):
			if self.tower_height>0:
				return self.rings[self.tower_height-1].position[2]
			return 0.0

		def tick(self):
			self.mgr_game.tick()
			self.mgr_render.render()

	GAME_OBJ=Game()
	return get_game()


