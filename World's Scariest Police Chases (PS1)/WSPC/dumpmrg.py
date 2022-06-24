
import struct, os

def strtab_get(strtab, off):
	return strtab[off:strtab.find(b"\0", off)]

def dump_mrg(path, folder):
	print(path, "=>", folder)
	os.makedirs(folder, exist_ok=True)
	data = open(path, "rb").read()
	count, = struct.unpack("I", data[0:4])
	for i in range(count):
		at = 4 + i * 12
		stroff, off, size = struct.unpack("III", data[at:at+12])
		name = strtab_get(data, stroff)
		print(name, off, size)
		open(folder + "/" + name.decode("utf-8"), "wb").write(data[off:off+size])


dump_mrg("police/MERGED/DAY_FLW.MRG", "dump/DAY_FLW.MRG")
dump_mrg("police/MERGED/DAWN_STD.MRG", "dump/DAWN_STD.MRG")

