
from pprint import pprint
from PIL import Image
import struct
import pygltflib

class TexPage:
	pass
class AtlasEntry:
	def __repr__(self):
		return "name_off=%d name=%s texpage=%d palette=%d x=%d y=%d w=%d h=%d" % (
			self.name_off, self.name, self.texpage, self.palette, self.x, self.y, self.w, self.h)
class Vertex:
	def __init__(self, p, c, t):
		self.p = p
		self.c = c
		self.t = t
	def __repr__(self):
		return "Vertex(p=%s c=%s t=%s)" % (self.p, self.c, self.t)
class Face:
	def __init__(self, v0, v1, v2, v3=None):
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.quad = v3 != None
	def __repr__(self):
		return "Face(quad=%s\nv0=%s\nv1=%s\nv2=%s\nv3=%s)" % (self.quad, self.v0, self.v1, self.v2, self.v3)
class Mesh:
	def __init__(self, name):
		self.name = name
		self.tris = []
		self.quads = []

def strtab_get(strtab, off):
	return strtab[off:strtab.find(b"\0", off)]

def expand_bitmap(bitmap):
	out = []
	for b in bitmap:
		out.append(b & 0xf)
		out.append(b >> 4)
	return out

def expand_palette(p):
	colors = [(p[i], p[i+1], p[i+2], 255 if p[i+3] else 0) for i in range(0, len(p), 4)]
	return [colors[i:i+16] for i in range(0, len(colors), 16)]

class DOB:
	def __init__(self, name):
		self.name = name
		self.texpages = []
		self.meshes = []

	def parse_section_image_data(self, data):
		unk1, unkcnt = struct.unpack("HH", data[:4])
		tp = TexPage()
		tp.unk_count = unkcnt
		tp.bitmap_orig = data[4:32768+4]
		tp.bitmap = expand_bitmap(tp.bitmap_orig)
		tp.palettes_orig = data[32768+4:]
		if len(tp.palettes_orig) != unkcnt * 4 * 16:
			print("UNKCNT != len(PALETTES)")
		tp.palettes = expand_palette(tp.palettes_orig)
		self.texpages.append(tp)

	def parse_section_image_strtab(self, data):
		self.img_strtab = data

	def parse_section_image_atlas(self, data):
		self.img_parts = []
		i = 0
		while i < len(data):
			entry = data[i:i+12]
			a = AtlasEntry()
			a.name_off, a.texpage, a.palette, a.x, a.y, a.w, a.h = struct.unpack("IHHBBBB", entry)
			a.name = strtab_get(self.img_strtab, a.name_off)
			self.img_parts.append(a)
			i += 12
		pprint(self.img_parts)

	def parse_section_model_data(self, data):
		self.model_data = data

	def parse_section_model_strtab(self, data):
		self.mdl_strtab = data

	def parse_section_model_metadata(self, data):
		for i in range(0, len(data), 56):
			entry = data[i:i+56]
			dec = struct.unpack("IIiii16xII8xI", entry)
			unk1, mesh_off, px, py, pz, bsr, name_off, unk2 = dec
			name = strtab_get(self.mdl_strtab, name_off)
			print(unk1, mesh_off, px, py, pz, bsr, name, unk2)
			if unk1 == 1:
				continue

			M = Mesh(name)
			M.px, M.py, M.pz = px, py, pz
			mdata = self.model_data[mesh_off:]

			#print("header:", struct.unpack("11I", mdata[:44]))
			dec2 = struct.unpack("7I", mdata[:28])
			unk1, num_pos, unk3, fcd_off, tex_off, unk4, pos_off = dec2
			print("model num_pos=%d pos_off=%d tex_off=%d fcd_off=%d" % (
				num_pos, pos_off, tex_off, fcd_off))

			bsr2, bx, by, bz, pa_off = struct.unpack("IhhhxxI", mdata[fcd_off:fcd_off+16])
			print("model face data header", bsr2, bx, by, bz, pa_off)

			pa_count, pa_list = struct.unpack("II", mdata[pa_off:pa_off+8])
			print("model face prim arr", pa_count, pa_list)

			def load_vert(idx, po, to, fdata):
				p = struct.unpack("hhh", mdata[po:po+6])
				co = 8 + idx * 4
				c = struct.unpack("BBB", fdata[co:co+3])
				to += 4 + idx * 2
				t = struct.unpack("BB", mdata[to:to+2])
				return Vertex(p, c, t)

			for j in range(pa_count):
				doff = pa_list + 8 * j
				dec3 = struct.unpack("BxxBI", mdata[doff:doff+8])
				fa_flags, fa_count, fa_off = dec3
				print("face arr", fa_flags, fa_count, fa_off)

				if fa_flags & 4: # quad
					for k in range(fa_count):
						fo = fa_off + k * 28
						fdata = mdata[fo:fo+28]
						dec4 = struct.unpack("BBHHH16xHH", fdata)
						unk1, unk2, po0, po1, po2, po3, to = dec4
						po0 += pos_off
						po1 += pos_off
						po2 += pos_off
						po3 += pos_off
						to += tex_off
						v0 = load_vert(0, po0, to, fdata)
						v1 = load_vert(1, po1, to, fdata)
						v2 = load_vert(2, po2, to, fdata)
						v3 = load_vert(3, po3, to, fdata)
						M.quads.append(Face(v0, v1, v3, v2))
				else: # tri
					for k in range(fa_count):
						fo = fa_off + k * 24
						fdata = mdata[fo:fo+24]
						dec4 = struct.unpack("BBHHH12xHxx", fdata)
						unk1, unk2, po0, po1, po2, to = dec4
						po0 += pos_off
						po1 += pos_off
						po2 += pos_off
						to += tex_off
						v0 = load_vert(0, po0, to, fdata)
						v1 = load_vert(1, po1, to, fdata)
						v2 = load_vert(2, po2, to, fdata)
						M.tris.append(Face(v0, v1, v2))
			pprint(M.quads)
			self.meshes.append(M)

		#v_pos = [struct.unpack("3h", data[i:i+6]) for i in range(off_pos, off_tex, 8)]
		#v_tex = [(data[i], data[i+1]) for i in range(off_tex, off_faces, 2)]
		#for i in range(off_faces, len(data), 28): print(i, len(data[i:i+28]))
		##v_fac = [struct.unpack("BB3H16BhBB", data[i:i+28]) for i in range(off_faces, len(data), 28)]
		#print("#pos=%d #tex=%d" % (len(v_pos), len(v_tex)))
		#pprint(v_pos)
		#pprint(v_tex)
		##pprint(v_fac)
		pass

	def parse_section(self, data, tab="", off=0):
		while len(data) >= 8:
			size, num = struct.unpack("II", data[:8])
			valid = ""
			if size < 8 or size > len(data):
				valid = "INVALID "
			if valid == "":
				print("%s%ssection off=%d size=%d num=%d preview=%s" % (tab, valid, off, size, num, data[8:min(size, 32)]))
			if size < 8:
				break
			sdata = data[8:size]
			if size <= len(data) and size >= 8:
				self.parse_section(sdata, tab + " ", off + 8)

			if num == 3: self.parse_section_image_data(sdata)
			if num == 14: self.parse_section_image_strtab(sdata)
			if num == 15: self.parse_section_image_atlas(sdata)
			if num == 5: self.parse_section_model_data(sdata)
			if num == 7: self.parse_section_model_strtab(sdata)
			if num == 6: self.parse_section_model_metadata(sdata)

			data = data[size:]
			off += size

	def parse_file(self):
		print(self.name)
		data = open(self.name, "rb").read()
		self.parse_section(data)
		return self

	def dump_atlas(self, path):
		imgs = []
		for _ in self.texpages:
			imgs.append(Image.new("RGBA", (256, 256)))
		for part in self.img_parts:
			img = imgs[part.texpage]
			tp = self.texpages[part.texpage]
			pal = tp.palettes[part.palette]
			for y in range(part.y, part.y + part.h):
				for x in range(part.x, part.x + part.w):
					pxi = tp.bitmap[x + y * 256]
					img.putpixel((x, y), pal[pxi])
		for i in range(len(imgs)):
			imgs[i].save(path + "[%d].png" % i)

	def dump_mesh(self, path):
		with open(path + ".obj", "w") as f:
			vo = 1
			for m in self.meshes:
				f.write("o %s\n" % m.name)
				for face in m.tris + m.quads:
					def write_vert(v):
						f.write("v %g %g %g %g %g %g\n" % (
							v.p[0] + m.px, v.p[1] + m.py, v.p[2] + m.pz,
							v.c[0] / 255, v.c[1] / 255, v.c[2] / 255))
						f.write("vt %g %g\n" % (v.t[0] / 255, 1 - v.t[1] / 255))
					write_vert(face.v0)
					write_vert(face.v1)
					write_vert(face.v2)
					if face.v3 is not None:
						write_vert(face.v3)
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


	def dump_all(self, path):
		self.dump_atlas(path)
		self.dump_mesh(path)

DOB("police/BACKDROP/06CLEAR.DOB").parse_file().dump_all("dump/06CLEAR.DOB")
DOB("police/BACKDROP/06CLOUDY.DOB").parse_file().dump_all("dump/06CLOUDY.DOB")
DOB("police/VEHICLES/AIPOLICE.DOB").parse_file().dump_all("dump/AIPOLICE.DOB")
#DOB("dump/DAY_FLW.MRG/MISC.DOB").parse_file().dump_all("dump/MISC.DOB")
#DOB("dump/DAWN_STD.MRG/MISC.DOB").parse_file().dump_all("dump/MISC.DOB")
