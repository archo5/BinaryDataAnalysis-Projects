
import struct, os

TOC = "POLICE.TOC"
IMG = "POLICE.IMG"

data = open(TOC, "rb").read()
img = open(IMG, "rb")

while len(data):
	name = data.split(b"\0", 1)[0]
	data = data[len(name)+1:]
	after = data[:8]
	data = data[8:]
	off, size = struct.unpack("<2i", after)
	img.seek(off)
	filedata = img.read(size)
	path = "police/" + name.replace(b"\\", b"/").decode("utf-8")
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "wb") as f:
		f.write(filedata)
	print("off %10d size %10d %s" % (
		off, size, name))
