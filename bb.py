#!/usr/bin/env python
import blib.window
import blib.game

from blib.object import Blob
from blib.colors import *


if __name__=="__main__":
	game=blib.game.get_game()
	blib.window.Initialize(game)
	Blob(1,green).add_to_world()
	blib.window.Run()
