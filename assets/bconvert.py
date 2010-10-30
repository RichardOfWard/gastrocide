import cPickle

import bpy
objects=list(bpy.data.objects)
store={}
faaa=None
for ob in objects:
	if ob.type=="Mesh":
		verts3=[]
		norms3=[]
		verts4=[]
		norms4=[]
		mesh = ob.getData(mesh=1)
		for face in mesh.faces:
			lv=verts4
			ln=norms4
			if len(face.verts)==3:
				lv=verts3
				ln=norms3
			for v in face.verts:
				lv+=list(v.co)
				if face.smooth:
					ln+=list(v.no)
				else:
					ln+=list(face.no)

		store[ob.name]=(verts3,norms3,verts4,norms4)

filename="blob.pkl"
f=file(filename,"wb")
cPickle.dump(store,f)
f.close()

