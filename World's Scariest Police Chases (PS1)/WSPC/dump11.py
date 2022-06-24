
import struct

with open("day-nth2", "rb") as f:
	with open("day-nth2-p1.obj", "w") as fo:
		for i in range(144):
			f.seek(140 + 20 * i)
			v = struct.unpack("hhh", f.read(6))
			fo.write("v %d %d %d\n" % v)
	with open("day-nth2-p2.obj", "w") as fo:
		for i in range(100):
			f.seek(3020 + i * 6)
			v = struct.unpack("hhh", f.read(6))
			fo.write("v %d %d %d\n" % v)
