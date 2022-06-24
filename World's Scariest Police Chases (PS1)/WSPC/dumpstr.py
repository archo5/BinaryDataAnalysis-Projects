
from pprint import pprint
from PIL import Image
import struct
import pygltflib

FILE = "DAY.STR"

TEXPAGE_SIZE = 2048

def expand_bitmap(bitmap):
	out = []
	for b in bitmap:
		out.append(b & 0xf)
		out.append(b >> 4)
	return out

def expand_palette(p):
	return [(p[i], p[i+1], p[i+2], 255 if p[i+3] else 0) for i in range(0, len(p), 4)]

def readat(f, at, sz):
	f.seek(at)
	return f.read(sz)

class StreamedFile:
	def __init__(self, f, i):
		self.index = i
		(self.x, self.y, self.off_links, fo) = struct.unpack("hhII", f.read(12))
		self.off_file = fo & 0x7ffffff
		self.fpg_tex = fo >> 27
	def __repr__(self):
		return "StreamedFile(#%d, x=%d, y=%d, off_links=%d, off_file=%d fpg_tex=%d)" % (
			self.index, self.x, self.y, self.off_links, self.off_file, self.fpg_tex)

class TextureSizes:
	def __init__(self, f):
		(self.size64, wh) = struct.unpack("BB", f.read(2))
		self.width16 = wh & 0xf
		self.height16 = wh >> 4
		self.size = self.size64 * 64
		self.width = self.width16 * 16
		self.height = self.height16 * 16
	def __repr__(self):
		return "TextureSizes(size=%d, w=%d, h=%d)" % (self.size, self.width, self.height)

class Vertex:
	def __init__(self, p, c, t):
		self.p = p
		self.c = c
		self.t = t
	def __repr__(self):
		return "Vertex(p=%s c=%s t=%s)" % (self.p, self.c, self.t)
class Face:
	def __init__(self, mtl, v0, v1, v2, v3=None):
		self.mtl = mtl
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.quad = v3 != None
	def __repr__(self):
		return "Face(mtl=%d\nquad=%s\nv0=%s\nv1=%s\nv2=%s\nv3=%s)" % (
			self.mtl, self.quad, self.v0, self.v1, self.v2, self.v3)
class Mesh:
	def __init__(self, name):
		self.px, self.py, self.pz = 0, 0, 0
		self.name = name
		self.tris = []
		self.quads = []

def dump_mesh(meshes, path):
	with open(path + ".obj", "w") as f:
		f.write("mtllib ~.mtl")
		vo = 1
		for m in meshes:
			f.write("o %s\n" % m.name)
			for face in m.tris + m.quads:
				def write_vert(v):
					f.write("v %g %g %g %g %g %g\n" % (
						v.p[0] + m.px, v.p[1] + m.py, v.p[2] + m.pz,
						v.c[0] / 255, v.c[1] / 255, v.c[2] / 255))
					f.write("vt %g %g\n" % (v.t[0], 1 - v.t[1]))
				write_vert(face.v0)
				write_vert(face.v1)
				write_vert(face.v2)
				if face.v3 is not None:
					write_vert(face.v3)
				f.write("usemtl %d\n" % face.mtl)
				f.write("f")
				def write_fv(at):
					f.write(" %d/%d" % (at, at))
				write_fv(vo)
				write_fv(vo + 1)
				write_fv(vo + 2)
				if face.quad:
					write_fv(vo + 3)
				f.write("\n")
				vo += 4 if face.quad else 3


with open("police/" + FILE, "rb") as archf:
	hdr = struct.unpack("11I", archf.read(44))
	(unk1, num_files, off_files, num_tex, off_texinfo,
		off_links, _, _, off_1stfile, off_textbl, off_unk) = hdr

	print("\n### parse texture lookup table ###")
	archf.seek(0)
	texlut = [struct.unpack("I", archf.read(4))[0] for i in range(0, off_links, 4)]

	def texlookup(x, y, z):
		a = texlut[off_textbl // 4 + x]
		b = texlut[a // 4 + y]
		c = texlut[b // 4 + z]
		#print("%d, %d, %d => %d, %d, %d" % (x, y, z, a, b, c))
		return c

	print("\n### parse file table ###")
	archf.seek(off_files)
	filetable = [StreamedFile(archf, i) for i in range(num_files)]
	#pprint(filetable)

	print("\n### parse texture size data ###")
	archf.seek(off_texinfo)
	texsizes = [TextureSizes(archf) for i in range(num_tex)]
	#pprint(texsizes)

	print("\n### generate material lib ###")
	if True:
		with open("dump/%s/~.mtl" % FILE, "w") as mtlf:
			for i in range(num_tex):
				mtlf.write("newmtl %d\n" % i)
				mtlf.write("Ka 1 1 1\n")
				mtlf.write("Kd 1 1 1\n")
				mtlf.write("Ks 0 0 0\n")
				mtlf.write("d 1\n")
				mtlf.write("illum 1\n")
				mtlf.write("map_Ka %d.png\n" % i)
				mtlf.write("map_Kd %d.png\n" % i)
				mtlf.write("map_d -imfchan m %d.png\n" % i)

	print("\n### parse textures ###")
	if False:
		texparsed = [False for i in range(num_tex)]
		for f in filetable:
			off_texarr = f.off_file + f.fpg_tex * TEXPAGE_SIZE
			archf.seek(off_texarr - 8)
			off_texidxarr = f.off_file + struct.unpack("I", archf.read(4))[0]
			archf.seek(off_texidxarr)
			num_texidx = struct.unpack("H", archf.read(2))[0]
			texidcs = struct.unpack("%dH" % num_texidx, archf.read(num_texidx * 2))
			print(num_texidx, texidcs)
			if f.off_file != 55296:
				break
			continue
			break
			archf.seek(off_texarr)
			for ti in texidcs:
				texsize = texsizes[ti]
				data = archf.read(texsize.size)
				if texparsed[ti]:
					continue
				print("- %d from file %d" % (ti, f.off_file))
				texparsed[ti] = True
				bitmap = expand_bitmap(data[:-64])
				palette = expand_palette(data[-64:])
				img = Image.new("RGBA", (texsize.width, texsize.height))
				for y in range(texsize.height):
					for x in range(texsize.width):
						pxi = bitmap[x + y * texsize.width]
						img.putpixel((x, y), palette[pxi])
				img.save("dump/%s/%d.png" % (FILE, ti))
	#

	print("\n### parse meshes ###")
	if False:
		allmeshes_hi = []
		allmeshes_lo = []
		allmeshes_misc = []
		for f in filetable:
			#if f.index != 37 and f.index != 1: continue

			# read texture indices first
			off_texarr = f.off_file + f.fpg_tex * TEXPAGE_SIZE
			archf.seek(off_texarr - 8)
			off_texidxarr = f.off_file + struct.unpack("I", archf.read(4))[0]
			archf.seek(off_texidxarr)
			num_texidx = struct.unpack("H", archf.read(2))[0]
			texidcs = struct.unpack("%dH" % num_texidx, archf.read(num_texidx * 2))
			print("#texidcs: %d" % len(texidcs))
			print(texidcs)

			tex_x = struct.unpack("I", readat(archf, f.off_file, 4))[0]
			bo = f.off_file + 4
			off_cur_file = 0
			meshes = []
			while True:
				archf.seek(bo + off_cur_file)
				fhdr = struct.unpack("13i", archf.read(52))
				(etype, dataoff, wx, wy, wz, _, _, _, _, bsrad,
					off_str2, off_nextfile, off_str1) = fhdr
				name = readat(archf, bo + off_str2, 64)
				name = name[:name.find(b"\0")].decode("utf-8")
				name2 = readat(archf, bo + off_str1, 64)
				name2 = name2[:name2.find(b"\0")].decode("utf-8")
				print("\n$ NODE", etype, off_nextfile, name, name2, wx, wy, wz)
				if etype == 7:
					print("--- %s/%s %d from file %d" % (name, name2, off_cur_file, f.off_file))
					print(fhdr)

					dec2 = struct.unpack("7I", readat(archf, bo + dataoff, 7 * 4))
					num_parts, num_pos, num_texco, fcd_off, tex_off, unk4, pos_off = dec2
					print("model num_parts=%d num_pos=%d pos_off=%d tex_off=%d fcd_off=%d" % (
						num_parts, num_pos, pos_off, tex_off, fcd_off))

					M = Mesh(name)
					for pid in range(num_parts):
						bsr2, bx, by, bz, u_1, u_2, pa_off, u_3 = struct.unpack(
							"IhhhBBII", readat(archf, bo + fcd_off + 20 * pid, 20))
						print("model face data header", bsr2, bx, by, bz, pa_off, "| UNK:", u_1, u_2, u_3)
						assert u_1 == 0 and u_2 == 0

						pa_count, pa_list = struct.unpack("II", readat(archf, bo + pa_off, 8))
						print("model face prim arr", pa_count, pa_list)

						archf.seek(bo + pos_off)
						scale = 4 if "GHS" in name else 1
						verts = [struct.unpack("hhhxx", archf.read(8)) for i in range(num_pos)]
						for i in range(len(verts)):
							v = verts[i]
							verts[i] = ((v[0] + wx) * scale, (v[1] + wy) * scale, (v[2] + wz) * scale)
						archf.seek(bo + tex_off)
						texcoords = [struct.unpack("16B", archf.read(16)) for i in range(num_texco)]
						#print(verts)
						#print(texcoords)
						#print([t[0] for t in texcoords])
						#print([t[2] for t in texcoords])

						def load_vert(tsd, idx, pid, tid, fdata):
							co = 8 + idx * 4
							c = struct.unpack("BBB", fdata[co:co+3])
							tx = texcoords[tid][idx*2+4]
							ty = texcoords[tid][idx*2+5]
							return Vertex(verts[pid], c, (tx / tsd.width, ty / tsd.height))

						for j in range(pa_count):
							doff = pa_list + 8 * j
							dec3 = struct.unpack("BBBBI", readat(archf, bo + doff, 8))
							fa_flags, u_3, u_4, fa_count, fa_off = dec3
							print("face arr", fa_flags, fa_count, fa_off, "| UNK:", u_3, u_4)

							archf.seek(bo + fa_off)
							if fa_flags & 4: # quad
								for k in range(fa_count):
									fdata = archf.read(28)
									dec4 = struct.unpack("BBHHH16xHH", fdata)
									unk1, unk2, po0, po1, po2, po3, to = dec4
									#print(unk1, unk2, (unk2 << 8) | unk1)
									po0 //= 8
									po1 //= 8
									po2 //= 8
									po3 //= 8
									to //= 16
									tid = texlookup(tex_x, texcoords[to][0], texcoords[to][2])
									tsd = texsizes[tid]
									v0 = load_vert(tsd, 0, po0, to, fdata)
									v1 = load_vert(tsd, 1, po1, to, fdata)
									v2 = load_vert(tsd, 2, po2, to, fdata)
									v3 = load_vert(tsd, 3, po3, to, fdata)
									M.quads.append(Face(tid, v0, v1, v3, v2))
							else: # tri
								for k in range(fa_count):
									fdata = archf.read(24)
									dec4 = struct.unpack("BBHHH12xHxx", fdata)
									unk1, unk2, po0, po1, po2, to = dec4
									#print(unk1, unk2, (unk2 << 8) | unk1)
									po0 //= 8
									po1 //= 8
									po2 //= 8
									to //= 16
									tid = texlookup(tex_x, texcoords[to][0], texcoords[to][2])
									tsd = texsizes[tid]
									v0 = load_vert(tsd, 0, po0, to, fdata)
									v1 = load_vert(tsd, 1, po1, to, fdata)
									v2 = load_vert(tsd, 2, po2, to, fdata)
									M.tris.append(Face(tid, v0, v1, v2))
					meshes.append(M)
					if "GFS" in M.name: allmeshes_hi.append(M)
					elif "GHS" in M.name: allmeshes_lo.append(M)
					else: allmeshes_misc.append(M)
				elif etype == 11:
					pass
				if not off_nextfile: break
				off_cur_file = off_nextfile
			#
			dump_mesh(meshes, "dump/%s/%d" % (FILE, f.index))
			if f.off_file > 52500000:
				break
		dump_mesh(allmeshes_hi, "dump/%s/~hi" % (FILE))
		dump_mesh(allmeshes_lo, "dump/%s/~lo" % (FILE))
		dump_mesh(allmeshes_misc, "dump/%s/~misc" % (FILE))
	#
