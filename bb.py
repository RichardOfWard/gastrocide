#!/usr/bin/env python
import blib.window
import blib.game

if __name__=="__main__":
	game=blib.game.get_game()
	blib.window.Initialize(game)
	game.load()
	blib.window.Run()
