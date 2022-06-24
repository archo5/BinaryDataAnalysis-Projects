import csv
import numpy as np

with open("rmi-entries.csv") as f:
	reader = csv.reader(f)
	data = list(reader)

with open("rmi-entries.obj", "w") as o:
	o.write("usemtl rmimtl\n")
	i = 0
	for line in data:
		#print(line)
		o.write("o obb%d\n" % i)
		r00, r10, r20, r01, r11, r21, r02, r12, r22, px, py, pz, _, _, _, sx, sy, sz = line[:18]
		pos = np.array([px, py, pz], dtype="float32")
		scl = np.array([sx, sy, sz], dtype="float32")
		#rm = np.matrix([[r00, r10, r20], [r01, r11, r21], [r02, r12, r22]])
		bvx = np.array([r00, r10, r20], dtype="float32") * float(sx)
		bvy = np.array([r01, r11, r21], dtype="float32") * float(sy)
		bvz = np.array([r02, r12, r22], dtype="float32") * float(sz)
		v000 = pos - bvx - bvy - bvz
		v001 = pos - bvx - bvy + bvz
		v010 = pos - bvx + bvy - bvz
		v011 = pos - bvx + bvy + bvz
		v100 = pos + bvx - bvy - bvz
		v101 = pos + bvx - bvy + bvz
		v110 = pos + bvx + bvy - bvz
		v111 = pos + bvx + bvy + bvz
		for v in [v000, v001, v010, v011, v100, v101, v110, v111]:
			o.write("v %g %g %g\n" % (v[0], v[1], v[2]))
		o.write("f {0} {1} {2} {3}\n".format(i*8+3, i*8+4, i*8+2, i*8+1))
		o.write("f {0} {1} {2} {3}\n".format(i*8+5, i*8+6, i*8+8, i*8+7))
		o.write("f {0} {1} {2} {3}\n".format(i*8+1, i*8+2, i*8+6, i*8+5))
		o.write("f {0} {1} {2} {3}\n".format(i*8+3, i*8+4, i*8+8, i*8+7))
		o.write("f {0} {1} {2} {3}\n".format(i*8+1, i*8+3, i*8+7, i*8+5))
		o.write("f {0} {1} {2} {3}\n".format(i*8+2, i*8+4, i*8+8, i*8+6))
		i += 1
