
import struct

data = open("C7-1__MAIN.GMS.dec", "rb").read()

def find_all(a_str, sub):
	start = 0
	while True:
		start = a_str.find(sub, start)
		if start == -1: return
		yield start
		start += len(sub)

def readu32(data, at):
	return struct.unpack("I", data[at:at+4])[0]

TMASK = 0xf
P1 = True
ref8list = []
refBlist = []
def try_parse(data, start, end):
	i = start
	while i < end:
		T = data[i]
		i += 1
		if P1: print("-", "[%X]" % (T >> 4), end="")
		if (T & TMASK) == 1: # double
			if P1: print("double:", struct.unpack("d", data[i:i+8])[0])
			i += 8
		elif (T & TMASK) == 2: # float
			if P1: print("float:", struct.unpack("f", data[i:i+4])[0])
			i += 4
		elif (T & TMASK) == 3: # int32
			v = struct.unpack("i", data[i:i+4])[0]
			if P1: print("int32: %d (%08X)" % (v, v))
			i += 4
		elif (T & TMASK) == 4: # uint8
			v = data[i]
			if P1: print("int32: %d (%08X)" % (v, v))
			i += 1
		elif (T & TMASK) == 8: # int32 REF 8
			v = struct.unpack("I", data[i:i+4])[0]
			if P1: print("REF_8: %08X (val=%d flags=%02X)" % (v, v & 0xffffff, v >> 24))
			if end - start != 26: ref8list.append(v & 0xffffff)
			i += 4
		elif (T & TMASK) == 9: # int32 REF 9
			v = struct.unpack("I", data[i:i+4])[0]
			if P1: print("REF_9: %08X (val=%d flags=%02X)" % (v, v & 0xffffff, v >> 24))
			i += 4
		elif (T & TMASK) == 0xA: # int32 REF A
			v = struct.unpack("I", data[i:i+4])[0]
			if P1: print("REF_A: %08X (val=%d flags=%02X)" % (v, v & 0xffffff, v >> 24))
			i += 4
		elif (T & TMASK) == 0xB: # int32 REF B
			v = struct.unpack("I", data[i:i+4])[0]
			if P1: print("REF_B: %08X (val=%d flags=%02X)" % (v, v & 0xffffff, v >> 24))
			if end - start != 26: refBlist.append(v & 0xffffff)
			i += 4
		else:
			if P1: print("UNKNOWN: %02X" % T)

count = 0
countfound = 0
prev = 0
for pos in find_all(data, b"\x06\xFF"):
	count += 1
	print(pos)
	i = prev#pos - 4
	while i < pos - 4:#i > prev:
		L = readu32(data, i)
		if L == pos + 2 - i:
			print("FOUND block size=%d at=%d" % (L, i))
			try_parse(data, i + 4, pos)
			countfound += 1
			break
		i += 1#-=
	prev = pos

print("total: %d, valid: %d" % (count, countfound))

print("ref 8 list:", sorted(ref8list))
print("ref B list:", sorted(refBlist))
