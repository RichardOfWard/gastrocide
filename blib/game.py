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
		def tick(self):
			self.mgr_game.tick()
			self.mgr_render.render()

	GAME_OBJ=Game()
	return get_game()


