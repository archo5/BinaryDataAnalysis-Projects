import csv

with open("rmi-qaabbs.csv") as f:
	reader = csv.reader(f)
	data = list(reader)

with open("rmi-qaabbs.obj", "w") as o:
	o.write("usemtl rmimtl\n")
	i = 0
	for line in data:
		#print(line)
		o.write("o qaabb%d\n" % i)
		x0, y0, z0, x1, y1, z1 = line[:6]
		x0 = float(x0)
		y0 = float(y0)
		z0 = float(z0)
		x1 = float(x1)
		y1 = float(y1)
		z1 = float(z1)
		v000 = (x0, y0, z0)
		v001 = (x0, y0, z1)
		v010 = (x0, y1, z0)
		v011 = (x0, y1, z1)
		v100 = (x1, y0, z0)
		v101 = (x1, y0, z1)
		v110 = (x1, y1, z0)
		v111 = (x1, y1, z1)
		for v in [v000, v001, v010, v011, v100, v101, v110, v111]:
			o.write("v %g %g %g\n" % (v[0], v[1], v[2]))
		o.write("f {0} {1} {2} {3}\n".format(i*8+3, i*8+4, i*8+2, i*8+1))
		o.write("f {0} {1} {2} {3}\n".format(i*8+5, i*8+6, i*8+8, i*8+7))
		o.write("f {0} {1} {2} {3}\n".format(i*8+1, i*8+2, i*8+6, i*8+5))
		o.write("f {0} {1} {2} {3}\n".format(i*8+3, i*8+4, i*8+8, i*8+7))
		o.write("f {0} {1} {2} {3}\n".format(i*8+1, i*8+3, i*8+7, i*8+5))
		o.write("f {0} {1} {2} {3}\n".format(i*8+2, i*8+4, i*8+8, i*8+6))
		i += 1
