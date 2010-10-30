from OpenGL.GLUT import *
from OpenGL.GL import *

from blib.colors import *

def Initialize(game):
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(1024,768)
	W=glutCreateWindow("Loading... Please WEIGHT!")
	def DisplayFunc(*args):
		try:
			glClearColor(*skyblue)
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			game.tick()
			glutSwapBuffers()
		except:
			import traceback
			import sys
			traceback.print_exc()
			sys.exit(1)
	def IdleFunc(*args):
		glutPostRedisplay()
	glutDisplayFunc(DisplayFunc)

	glutIdleFunc(IdleFunc)

	glEnable(GL_LIGHTING)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_DEPTH_TEST)

def Run():
	glutMainLoop()
