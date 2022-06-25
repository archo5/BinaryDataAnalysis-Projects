
import os, struct
from PIL import Image

os.chdir("E:/HRT")

def expand_bitmap(bitmap):
	out = []
	for b in bitmap:
		out.append(b & 0xf)
		out.append(b >> 4)
	return out

def rgb555_to_pil_color(c):
	if c == 0:
		return (0, 0, 0, 0)
	r = ((c >> 0) & 0x1f) << 3
	g = ((c >> 5) & 0x1f) << 3
	b = ((c >> 10) & 0x1f) << 3
	return (r, g, b, 255)

def tim_to_png(f, path):
	assert(f.read(4) == b"\x10\0\0\0")
	type = f.read(4)
	if type == b"\2\0\0\0":
		if os.path.exists(path): return
		f.read(8) # skip unknown/position
		size = struct.unpack("HH", f.read(4))
		img = Image.new("RGBA", size)
		src = struct.unpack("%dH" % (size[0] * size[1]), f.read(size[0] * size[1] * 2))
		print("> [%d] %s : %s" % (type[0], path, size))
		for y in range(size[1]):
			for x in range(size[0]):
				img.putpixel((x, y), rgb555_to_pil_color(src[x + size[0] * y]))
		img.save(path)
	elif type == b"\x08\0\0\0" or type == b"\x09\0\0\0":
		if os.path.exists(path): return
		clutsize = 16 if type == b"\x08\0\0\0" else 256
		f.read(10) # skip unknown/position
		ncluts = struct.unpack("H", f.read(2))[0]
		clutdata = f.read(clutsize * 2 * ncluts)
		pal1 = struct.unpack("%dH" % clutsize, clutdata[:clutsize * 2])
		palc = [rgb555_to_pil_color(c) for c in pal1]
		f.read(8) # skip unknown/position
		rowwidth, height = struct.unpack("HH", f.read(4))
		rowwidth *= 2
		width = rowwidth
		nbytes = rowwidth * height
		idxmap = struct.unpack("%dB" % (nbytes), f.read(nbytes))
		if type == b"\x08\0\0\0":
			idxmap = expand_bitmap(idxmap)
			width *= 2
		size = (width, height)
		print("> [%d] %s : %s" % (type[0], path, size))
		img = Image.new("RGBA", size)
		for y in range(height):
			for x in range(width):
				img.putpixel((x, y), palc[idxmap[x + y * width]])
		img.save(path)
	else:
		print(type)

for root, dirs, files in os.walk("."):
	for file in files:
		if file.endswith(".TIM"):
			path = os.path.join(root, file)
			print(path)
			with open(path, "rb") as TIM:
				tim_to_png(TIM, "%s.png" % (path))
		if file.endswith(".TMM"):
			path = os.path.join(root, file)
			print(path)
			with open(path, "rb") as TMM:
				assert(TMM.read(4) == b"TMM\x10")
				count = struct.unpack("I", TMM.read(4))[0]
				print("images:", count)
				print("metadata:", struct.unpack("HHHHHHHH", TMM.read(16)))
				offsets = struct.unpack("%dI" % count, TMM.read(4 * count))
				#print("offsets:", offsets)
				for i, off in enumerate(offsets):
					TMM.seek(off)
					tim_to_png(TMM, "%s-%d.png" % (path, i))
