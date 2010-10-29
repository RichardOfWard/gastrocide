#!/usr/bin/env python
import blib.window
import blib.game

from blib.object import Triangle,MeshModel


if __name__=="__main__":
	game=blib.game.get_game()
	blib.window.Initialize(game)
	MeshModel("blob").add_to_world()
	blib.window.Run()
