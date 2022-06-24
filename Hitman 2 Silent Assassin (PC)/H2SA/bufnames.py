
data = open("C7-1__MAIN.BUF", "rb").read()

# is name char?
def NC(v):
	return v > 0x20 and v < 0x7f and v != 0x3f # skip '?'

def readuntil0(data, i):
	end = i
	while data[end]:
		end += 1
	return data[i:end]

count = 0
for i in range(20664, len(data) - 5):
	if not NC(data[i]) and NC(data[i+1]) and NC(data[i+2]) and NC(data[i+3]) and NC(data[i+4]):
		print("%d: %s" % (i + 1, readuntil0(data, i + 1)))
		count += 1
print(count)
