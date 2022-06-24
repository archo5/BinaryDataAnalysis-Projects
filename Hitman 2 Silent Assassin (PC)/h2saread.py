
import struct, bdat, h2sa
from pprint import pprint

DATA = open("E:/H2SA/SCENES/C7-1/C7-1__MAIN.PRM", "rb").read()
HDR, _ = bdat.read_struct(h2sa.prm_hdr, DATA, 0)
mesh = HDR.meshes[1104]

def expand_tristrip(a):
	o = []
	flip = False
	for i in range(2, len(a)):
		if flip:
			o.append(a[i - 1])
			o.append(a[i - 2])
			o.append(a[i])
		else:
			o.append(a[i - 2])
			o.append(a[i - 1])
			o.append(a[i])
		flip ^= True
	return o

obj = ""
for i in range(mesh.vcount):
	off = mesh.voff + i * 36
	v = struct.unpack("3f3f4B2f", DATA[off: off + 36])
	obj += "v %g %g %g\n" % (v[0], v[1], v[2])
	obj += "vn %g %g %g\n" % (v[3], v[4], v[5])
	obj += "vt %g %g\n" % (v[10], 1 - v[11])
idcs = [struct.unpack("H", DATA[mesh.ioff + i * 2: mesh.ioff + i * 2 + 2])[0]
	for i in range(mesh.numidxvals)]
if idcs[0] == 1:
	idcs = idcs[2:]
print(idcs)
idcs = expand_tristrip(idcs)
print(idcs)
for i in range(0, len(idcs), 3):
	i0 = idcs[i]
	i2 = idcs[i + 1]
	i1 = idcs[i + 2]
	obj += "f {0}/{0}/{0} {1}/{1}/{1} {2}/{2}/{2}\n".format(i0 + 1, i1 + 1, i2 + 1)
print(obj)
open("h2sa.obj", "w").write(obj)
