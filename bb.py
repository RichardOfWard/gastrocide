#!/usr/bin/env python
import blib.window
import blib.game

from blib.object import PlayerBlob, RingLevel, MeshModel, Tower
from blib.colors import *


if __name__=="__main__":
	game=blib.game.get_game()
	blib.window.Initialize(game)
	Tower().add_to_world()
	PlayerBlob().add_to_world()
	RingLevel().add_to_world()
	blib.window.Run()
