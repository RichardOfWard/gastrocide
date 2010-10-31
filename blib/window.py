from OpenGL.GLUT import *
from OpenGL.GL import *
import time

from blib.colors import *

import sys

last_tick=time.time()

def Initialize(game):
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(1024,768)
	W=glutCreateWindow("GastroCide!")
	def DisplayFunc(*args):
		try:
			glClearColor(*skyblue)
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			game.tick()
			glutSwapBuffers()
			global last_tick
			last_tick=time.time()
		except:
			import traceback
			import sys
			traceback.print_exc()
			sys.exit(1)
	glutDisplayFunc(DisplayFunc)

	def IdleFunc(*args):
		while time.time()-last_tick<1.0/70.0:
			pass
		glutPostRedisplay()
	glutIdleFunc(IdleFunc)

	glutSetKeyRepeat(False)
	glutkeys={}
	glutkeys[GLUT_KEY_UP]="up"
	glutkeys[GLUT_KEY_DOWN]="down"
	glutkeys[GLUT_KEY_LEFT]="left"
	glutkeys[GLUT_KEY_RIGHT]="right"
	def SpecialFunc(key,x,y):
		key=glutkeys.get(key,None)
		if key is not None:
			game.keys[key]=True
	def SpecialUpFunc(key,x,y):
		key=glutkeys.get(key,None)
		if key is not None:
			game.keys[key]=False
	glutSpecialFunc(SpecialFunc)
	glutSpecialUpFunc(SpecialUpFunc)
	def KeyFunc(key,x,y):
		if key in game.keys.keys():
			game.keys[key]=True
		if key=='\x1b':
			sys.exit()
	def KeyUpFunc(key,x,y):
		if key in game.keys.keys():
			game.keys[key]=False
	glutKeyboardFunc(KeyFunc)
	glutKeyboardUpFunc(KeyUpFunc)

	glEnable(GL_LIGHTING)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_DEPTH_TEST)
	glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glEnable(GL_NORMALIZE)

def Run():
	glutMainLoop()
