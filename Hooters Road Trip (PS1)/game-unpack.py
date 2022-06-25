
import os, struct

os.chdir("E:/HRT")

def nullterm(b: bytes):
	return b.split(b"\0", 1)[0].decode("utf-8")

def process_entry(G, prefix):
	name, _, off, size, _, unkfv = struct.unpack(">12sIIIII", G.read(32))
	name = nullterm(name)
	path = prefix + "/" + name
	bk = G.tell()
	G.seek(off)
	if unkfv == 0:
		# directory
		print(">", path)
		os.makedirs(path, exist_ok=True)
		for i in range(size):
			process_entry(G, path)
	else:
		# file
		print("writing file", path)
		with open(path, "wb") as O:
			O.write(G.read(size))
	G.seek(bk)

with open("GAME.DAT", "rb") as G:
	assert(G.read(4) == b"MFS ")
	startoff = struct.unpack(">I", G.read(4))[0]
	print("start off:", startoff)
	G.read(4 * 6) # unknown
	bk = G.tell()
	rootstart = None
	rootend = None
	while G.tell() < startoff:
		p = G.tell()
		name, unk0, off, size, unk1, unk2 = struct.unpack(">12sIIIII", G.read(32))
		name = nullterm(name)
		if name == "----ROOT----":
			rootstart = p
			rootend = off
		print("entry: %12s ?=%d off=%d size=%d ?=%d ?=%d" % (
			name, unk0, off, size, unk1, unk2))
	# this time do a tree-based read
	G.seek(rootstart)
	while G.tell() < rootend:
		process_entry(G, "game")
