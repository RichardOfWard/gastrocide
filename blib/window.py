import OpenGL.GLUT as glut
import OpenGL.GL as gl

def Initialize(game):
	glut.glutInit()
	glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
	glut.glutInitWindowSize(1024,768)
	W=glut.glutCreateWindow("Loading... Please WEIGHT!")
	def DisplayFunc(*args):
		try:
			gl.glClearColor(0,0,0,0)
			gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
			game.tick()
			glut.glutSwapBuffers()
		except:
			import traceback
			import sys
			traceback.print_exc()
			sys.exit(1)
	def IdleFunc(*args):
		glut.glutPostRedisplay()
	glut.glutDisplayFunc(DisplayFunc)
	glut.glutIdleFunc(IdleFunc)

def Run():
	glut.glutMainLoop()
