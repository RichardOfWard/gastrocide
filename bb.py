#!/usr/bin/env python
import blib.window
import blib.game

from ctypes import util
try:
    from OpenGL.platform import win32
except AttributeError:
    pass


if __name__=="__main__":
	game=blib.game.get_game()
	blib.window.Initialize(game)
	game.load()
	blib.window.Run()
