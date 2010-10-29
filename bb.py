#!/usr/bin/env python
import blib.window
import blib.game

from blib.object import Triangle


if __name__=="__main__":
	game=blib.game.get_game()
	game.mgr_render.add_object(Triangle())
	blib.window.Initialize(game)
