GAME_OBJ=None
def get_game():
	global GAME_OBJ
	if GAME_OBJ is not None:
		return GAME_OBJ

	from blib.mgr import MgrRender
	class Game:
		def __init__(self):
			self.mgr_render=MgrRender()
		def tick(self):
			self.mgr_render.render()

	GAME_OBJ=Game()
	return get_game()


