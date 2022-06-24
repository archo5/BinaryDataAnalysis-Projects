import csv

with open("sgp-links.csv") as f:
	reader = csv.reader(f)
	data = list(reader)

with open("sgp-links.obj", "w") as o:
	i = 0
	for line in data:
		#print(line)
		o.write("o gate%d\n" % i)
		o.write("v {0} {1} {2}\nv {3} {4} {5}\nv {6} {7} {8}\nv {9} {10} {11}\n".format(*line))
		o.write("f {0} {1} {2} {3}\n".format(i * 4 + 1, i * 4 + 2, i * 4 + 3, i * 4 + 4))
		i += 1
