from distutils.core import setup
import py2exe

setup(windows=['bb.py'],
		options={
			"py2exe": {
				"includes": ["ctypes", "logging"],
				"excludes": ["OpenGL"],
				}
			}
		)

