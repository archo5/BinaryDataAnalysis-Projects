
import struct, csv

FILES = [
	("day-first", 4),
	("day-first", 72),
	("day-2nd", 4),
	("day-2nd", 6824),
	("day-2nd", 20472),
	("day-2nd", 20992),
	("day-2nd", 21752),
	("day-2nd", 21832),
	("day-2nd", 21916),
	("day-2nd", 22000),
	("day-2nd", 22084),
	("day-2nd", 22168),
	("day-2nd", 22252),
	("day-2nd", 22336),
	("day-2nd", 24156),
	("day-2nd", 24236),
	("day-2nd", 25944),
	("day-nth2", 4),
	("day-nth2", 0x1124),
	("day-nth2", 0x1774),
	("day-nth2", 0x1FBC),
]
LENGTH = 0x70

rows = [[]]

for fe in FILES:
	rows[0].append("offset")
	rows[0].append("%s@%d" % (fe[0], fe[1]))
	rows[0].append("notes")

fileinfo = [(fe[0], open(fe[0], "rb"), fe[1]) for fe in FILES]
for f in fileinfo:
	f[1].seek(f[2])
for i in range(0, LENGTH, 4):
	row = []
	for f in fileinfo:
		row.append(f[1].tell() - 4)
		row.append(struct.unpack("i", f[1].read(4))[0])
		row.append("")
	rows.append(row)

with open("strf-intro-compare.csv", "w", newline="") as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for row in rows:
		csv_writer.writerow(row)
