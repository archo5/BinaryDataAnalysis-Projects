
import struct, csv

FILES = {
	"DAY.STR": 0x3ADC, # 15068
	"DAWN.STR": 0x3ADC, # 15068
	"NIGHT.STR": 0x3AC0, # 15040
	"RAIN.STR": 0x3AC4, # 15044
}

rows = []

fileinfo = [(k, open("police/" + k, "rb"), FILES[k]) for k in FILES]
while True:
	row = []
	for f in fileinfo:
		val = struct.unpack("I", f[1].read(4))[0] if f[1].tell() < f[2] else ""
		row.append(val)
	if str(row) == "['', '', '', '']":
		break
	else:
		print(str(row))
	rows.append(row)

with open("str-intro-compare.csv", "w", newline="") as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(["file off"] + [f[0] for f in fileinfo])
	csv_writer.writerow([""] + ["lim %d" % f[2] for f in fileinfo])
	csv_writer.writerow([""] + ["# %d" % (f[2] // 4) for f in fileinfo])
	csv_writer.writerow([""] + ["" for f in fileinfo])
	off = 0
	for row in rows:
		csv_writer.writerow([off] + row)
		off += 4


fileinfo[0][1].seek(34000)
fileinfo[1][1].seek(34000)
fileinfo[2][1].seek(33960)
fileinfo[3][1].seek(33964)
with open("str-6-compare.csv", "w", newline="") as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow([f[0] for f in fileinfo])
	for _ in range(1354):
		row = []
		for f in fileinfo:
			row.append(struct.unpack("I", f[1].read(4))[0])
		csv_writer.writerow(row)

def bm(i, s):
	return "1" if i & (1 << s) else "0"

fp = fileinfo[0][1]
fp.seek(18756)
with open("str-3-compare.csv", "w", newline="") as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(["x", "y", "links off", "file off", "file off hex",
		"flag 1", "flag 2", "flag 3", "flag 4", "flag 5"])
	for _ in range(677):
		x, y, linksoff, fi = struct.unpack("hhII", fp.read(12))
		row = [x, y, linksoff, fi & 0x7ffffff, hex(fi & 0x7ffffff),
			bm(fi, 27), bm(fi, 28), bm(fi, 29), bm(fi, 30), bm(fi, 31)]
		csv_writer.writerow(row)
