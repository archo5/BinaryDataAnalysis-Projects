
import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def quad2tri(arr):
	out = []
	for i in range(0, len(arr), 4):
		out += [arr[i], arr[i+1], arr[i+3], arr[i+3], arr[i+2], arr[i]]
	return out

xd = []
yd = []
zd = []
pd = []
cd = []

data = open("section5_06clear", "rb").read()

#for i in range(600, 2100, 28):
#	xd.append(struct.unpack("h", data[i+8:i+10]))
#	yd.append(struct.unpack("h", data[i+6:i+8]))
#	zd.append(i)
#for i in range(524, 672, 2):
#	xd.append(data[i])
#	yd.append(data[i+1])
#	zd.append(0)
#for i in range(44, 516, 8):
#	xd.append(struct.unpack("h", data[i:i+2]))
#	yd.append(struct.unpack("h", data[i+2:i+4]))
#	zd.append(struct.unpack("h", data[i+4:i+6]))
for i in range(0x2C8, 0x838, 28):
	assert struct.unpack("h", data[i-6:i-4])[0] == data[i+0*4+3] * 8
	assert struct.unpack("h", data[i-4:i-2])[0] == data[i+1*4+3] * 8
	assert struct.unpack("h", data[i-2:i-0])[0] == data[i+2*4+3] * 8
	assert struct.unpack("h", data[i+16:i+18])[0] == data[i+3*4+3] * 8
	for j in range(4):
		v = data[i+j*4+3]
		vo = 44 + v * 8
		xd.append(struct.unpack("h", data[vo:vo+2])[0])
		yd.append(struct.unpack("h", data[vo+2:vo+4])[0])
		zd.append(struct.unpack("h", data[vo+4:vo+6])[0])
		#xd.append(struct.unpack("h", data[i-6:i-4])[0])
		#yd.append(struct.unpack("h", data[i-4:i-2])[0])
		#zd.append(struct.unpack("h", data[i-2:i-0])[0])
		cd.append((data[i+j*4+0] / 255, data[i+j*4+1] / 255, data[i+j*4+2] / 255))
		pd.append(struct.unpack("hhh", data[vo:vo+6]))
xd = quad2tri(xd)
yd = quad2tri(yd)
zd = quad2tri(zd)
pd = quad2tri(pd)
cd = quad2tri(cd)
verts = [list(zip(xd, yd, zd))]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(-10000, 10000)
ax.set_ylim3d(-10000, 10000)
ax.set_zlim3d(-10000, 10000)
#pc = Poly3DCollection([pd[i:i+3] for i in range(0, len(pd), 3)])
#ax.add_collection3d(pc)
ax.scatter(xd, yd, zd, c=cd)
plt.show()
