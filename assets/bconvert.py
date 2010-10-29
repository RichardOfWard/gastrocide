import cPickle

import bpy
objects=list(bpy.data.objects)
store={}
for ob in objects:
	if ob.type=="Mesh":
		verts3=[]
		verts4=[]
		mesh = ob.getData(mesh=1)
		for face in mesh.faces:
			l=verts4
			if len(face.verts)==3:
				l=verts3
			for v in face.verts:
				l+=list(v.co)
		store[ob.name]=(verts3,verts4)

filename="blob.pkl"
f=file(filename,"wb")
cPickle.dump(store,f)
f.close()

