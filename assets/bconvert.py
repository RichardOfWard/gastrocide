import cPickle

import bpy
objects=list(bpy.data.objects)
verts3=[]
verts4=[]
for ob in objects:
	if ob.type=="Mesh":
		mesh = ob.getData(mesh=1)
		for face in mesh.faces:
			l=verts4
			if len(face.verts)==3:
				l=verts3
			for v in face.verts:
				l+=list(v.co)

filename="blob.pkl"
f=file(filename,"wb")
cPickle.dump(verts3,f)
