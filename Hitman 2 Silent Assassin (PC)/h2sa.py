import bdat
class anm_anim(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_name = off
		self.name, off = bdat.read_builtin("char", src, off, 32, False)
		self._off_srcfile = off
		self.srcfile, off = bdat.read_builtin("char", src, off, 36, False)
		self._off_num = off
		self.num, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_unk2 = off
		self.unk2, off = bdat.read_builtin("i32", src, off, False, False)
		self._off_unk3 = off
		self.unk3, off = bdat.read_builtin("i32", src, off, False, False)
		self._off_unk4 = off
		self.unk4, off = bdat.read_builtin("f32", src, off, 3, False)
		self._off_unk5 = off
		self.unk5, off = bdat.read_builtin("i32", src, off, 5, False)
		self._off_unk6 = off
		self.unk6, off = bdat.read_builtin("u32", src, off, 4, False)
		self._off_offchanarr = off
		self.offchanarr, off = bdat.read_builtin("u32", src, off, False, False)
		vs = fdvs
		vs.vars['origOff'] = off
		vs.vars['i'] = 0
		cfo = ((bdat.me_structoff(vs, vs.root_query("anm_chunk", {"type":"5",}))+vs.get_variable([self], "offchanarr", 0, False))+(8))
		self._off_numchans = cfo
		self.numchans, _ = bdat.read_builtin("u32", src, cfo, False, False)
		vs = ipvs
		vs = fdvs
		vs.vars['origOff'] = off
		vs.vars['i'] = 0
		cfo = ((bdat.me_structoff(vs, vs.root_query("anm_chunk", {"type":"5",}))+(12))+vs.get_variable([self], "offchanarr", 0, False))
		self._off_chanoffs = cfo
		self.chanoffs, _ = bdat.read_builtin("u32", src, cfo, self.numchans+0, False)
		vs = ipvs
		vs = fdvs
		vs.vars['origOff'] = off
		cfo = []
		for i in range(self.numchans+0):
			vs.vars['i'] = i
			ceo = ((bdat.me_structoff(vs, vs.root_query("anm_chunk", {"type":"5",}))+(8))+vs.get_variable([self], "chanoffs", vs.get_variable([self], "i", 0, False), False))
			cfo.append(ceo)
		self._off_channels = cfo
		self.channels, _ = bdat.read_struct(anm_channel, src, cfo, self.numchans+0, False, {})
		self._offend = off


class anm_channel(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_boneoff = off
		self.boneoff, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_a = off
		self.a, off = bdat.read_builtin("u16", src, off, 2, False)
		self._off_numframes = off
		self.numframes, off = bdat.read_builtin("u16", src, off, False, False)
		self._off_flags = off
		self.flags, off = bdat.read_builtin("u16", src, off, False, False)
		if (vs.get_variable([self], "flags", 0, False)!=(28)) != 0:
			self._off_rotdataoff = off
			self.rotdataoff, off = bdat.read_builtin("u32", src, off, False, False)
		else:
			self.rotdataoff = None
		if (vs.get_variable([self], "flags", 0, False)!=(28)) != 0:
			self._off_rotidx1off = off
			self.rotidx1off, off = bdat.read_builtin("u32", src, off, False, False)
		else:
			self.rotidx1off = None
		if (vs.get_variable([self], "flags", 0, False)!=(28)) != 0:
			self._off_rotidx2off = off
			self.rotidx2off, off = bdat.read_builtin("u32", src, off, False, False)
		else:
			self.rotidx2off = None
		if (vs.get_variable([self], "flags", 0, False)==(5)) != 0:
			self._off_posdataoff = off
			self.posdataoff, off = bdat.read_builtin("u32", src, off, False, False)
		else:
			self.posdataoff = None
		if (vs.get_variable([self], "flags", 0, False)==(5)) != 0:
			self._off_posidx1off = off
			self.posidx1off, off = bdat.read_builtin("u32", src, off, False, False)
		else:
			self.posidx1off = None
		if (vs.get_variable([self], "flags", 0, False)==(5)) != 0:
			self._off_posidx2off = off
			self.posidx2off, off = bdat.read_builtin("u32", src, off, False, False)
		else:
			self.posidx2off = None
		if (vs.get_variable([self], "flags", 0, False)!=(28)) != 0:
			vs = fdvs
			vs.vars['origOff'] = off
			vs.vars['i'] = 0
			cfo = ((bdat.me_structoff(vs, vs.root_query("anm_chunk", {"type":"6",}))+(8))+vs.get_variable([self], "rotidx1off", 0, False))
			self._off_rotidcs1 = cfo
			self.rotidcs1, _ = bdat.read_builtin("u8", src, cfo, self.numframes+0, False)
		else:
			self.rotidcs1 = None
		vs = ipvs
		if (vs.get_variable([self], "flags", 0, False)!=(28)) != 0:
			vs = fdvs
			vs.vars['origOff'] = off
			vs.vars['i'] = 0
			cfo = ((bdat.me_structoff(vs, vs.root_query("anm_chunk", {"type":"6",}))+(8))+vs.get_variable([self], "rotidx2off", 0, False))
			self._off_rotidcs2 = cfo
			self.rotidcs2, _ = bdat.read_builtin("u8", src, cfo, self.numframes+0, False)
		else:
			self.rotidcs2 = None
		self._offend = off


class anm_chunk(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_type = off+0
		self.type, _ = bdat.read_builtin("u32", src, off+0, False, False)
		self._off_sizeflags = off+4
		self.sizeflags, _ = bdat.read_builtin("u32", src, off+4, False, False)
		self.size = (vs.get_variable([self], "sizeflags", 0, False)&(16777215))
		self.flags = (vs.get_variable([self], "sizeflags", 0, False)>>(24))
		if (vs.get_variable([self], "flags", 0, False)&(64)) != 0:
			self._off_start = off+8
			self.start, _ = bdat.read_builtin("u32", src, off+8, False, False)
		else:
			self.start = None
		if (vs.get_variable([self], "flags", 0, False)&(64)) != 0:
			self._off_numparts = off+12
			self.numparts, _ = bdat.read_builtin("u32", src, off+12, False, False)
		else:
			self.numparts = None
		if (vs.get_variable([self], "flags", 0, False)&(64)) != 0:
			self._off_partsizes = off+16
			self.partsizes, _ = bdat.read_builtin("u32", src, off+16, self.numparts+0, False)
		else:
			self.partsizes = None
		self._offend = TODO(size + sizeSrc)


class anm_file(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_count = off
		self.count, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_nameoff = off
		self.nameoff, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_animoffs = off
		self.animoffs, off = bdat.read_builtin("u32", src, off, self.count+0, False)
		vs = fdvs
		vs.vars['origOff'] = off
		vs.vars['i'] = 0
		cfo = (bdat.me_structoff(vs, [self])+vs.get_variable([self], "nameoff", 0, False))
		self._off_name = cfo
		self.name, _ = bdat.read_builtin("char", src, cfo, 64, True)
		vs = ipvs
		vs = fdvs
		vs.vars['origOff'] = off
		cfo = []
		for i in range(self.count+0):
			vs.vars['i'] = i
			ceo = ((bdat.me_structoff(vs, vs.root_query("anm_chunk", {"type":"5",}))+(8))+vs.get_variable([self], "animoffs", vs.get_variable([self], "i", 0, False), False))
			cfo.append(ceo)
		self._off_anims = cfo
		self.anims, _ = bdat.read_struct(anm_anim, src, cfo, self.count+0, False, {})
		self._offend = off


class loc_cat(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_name = off
		self.name, off = bdat.read_builtin("char", src, off, 64, True)
		self._off_count = off
		self.count, off = bdat.read_builtin("u8", src, off, False, False)
		self._off_offsets = off
		self.offsets, off = bdat.read_builtin("u32", src, off, self.count+-1, False)
		self._off_maps = off
		self.maps, off = bdat.read_struct(loc_map, src, off, self.count+0, False, {})
		self._offend = off


class loc_file(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_count = off
		self.count, off = bdat.read_builtin("u8", src, off, False, False)
		self._off_offsets = off
		self.offsets, off = bdat.read_builtin("u32", src, off, self.count+-1, False)
		vs = fdvs
		vs.vars['origOff'] = off
		cfo = []
		for i in range(self.count+0):
			vs.vars['i'] = i
			ceo = (vs.get_variable([self], "orig", 0, False)+vs.get_variable([self], "offsets", (vs.get_variable([self], "i", 0, False)-(1)), False))
			cfo.append(ceo)
		self._off_cats = cfo
		self.cats, _ = bdat.read_struct(loc_keyvalue, src, cfo, self.count+0, False, {})
		self._offend = off


class loc_keyvalue(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_key = off
		self.key, off = bdat.read_builtin("char", src, off, 64, True)
		self._off_count = off
		self.count, off = bdat.read_builtin("u8", src, off, False, False)
		if ((vs.get_variable([self], "count", 0, False)==(1))&(vs.get_variable([self], "depth", 0, False)>(1))) != 0:
			self._off_value = off
			self.value, off = bdat.read_builtin("char", src, off, 64, True)
		else:
			self.value = None
		if (vs.get_variable([self], "count", 0, False)>(1)) != 0:
			self._off_offsets = off
			self.offsets, off = bdat.read_builtin("u32", src, off, self.count+-1, False)
		else:
			self.offsets = None
		if ((vs.get_variable([self], "count", 0, False)>(1))|(vs.get_variable([self], "depth", 0, False)<=(1))) != 0:
			vs = fdvs
			vs.vars['origOff'] = off
			cfo = []
			for i in range(self.count+0):
				vs.vars['i'] = i
				ceo = (vs.get_variable([self], "orig", 0, False)+vs.get_variable([self], "offsets", (vs.get_variable([self], "i", 0, False)-(1)), False))
				cfo.append(ceo)
			self._off_children = cfo
			self.children, _ = bdat.read_struct(loc_keyvalue, src, cfo, self.count+0, False, {})
		else:
			self.children = None
		self._offend = off


class loc_map(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_name = off
		self.name, off = bdat.read_builtin("char", src, off, 64, True)
		self._off_count = off
		self.count, off = bdat.read_builtin("u8", src, off, False, False)
		self._off_offsets = off
		self.offsets, off = bdat.read_builtin("u32", src, off, self.count+-1, False)
		vs = fdvs
		vs.vars['origOff'] = off
		cfo = []
		for i in range(self.count+0):
			vs.vars['i'] = i
			ceo = (vs.get_variable([self], "orig", 0, False)+vs.get_variable([self], "offsets", (vs.get_variable([self], "i", 0, False)-(1)), False))
			cfo.append(ceo)
		self._off_entries = cfo
		self.entries, _ = bdat.read_struct(loc_keyvalue, src, cfo, self.count+0, False, {})
		self._offend = off


class mesh(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_ext1off = off+24
		self.ext1off, _ = bdat.read_builtin("u32", src, off+24, False, False)
		self._off_voff = off+28
		self.voff, _ = bdat.read_builtin("u32", src, off+28, False, False)
		self._off_ioff = off+68
		self.ioff, _ = bdat.read_builtin("u32", src, off+68, False, False)
		self._off_vcount = off+22
		self.vcount, _ = bdat.read_builtin("u16", src, off+22, False, False)
		vs = fdvs
		vs.vars['origOff'] = off+0
		vs.vars['i'] = 0
		cfo = vs.get_variable([self], "ioff", 0, False)
		self._off_firstidx = cfo
		self.firstidx, _ = bdat.read_builtin("u16", src, cfo, False, False)
		vs.vars['origOff'] = off+0
		vs.vars['i'] = 0
		cfo = (vs.get_variable([self], "ioff", 0, False)+((vs.get_variable([self], "firstidx", 0, False)==(1))*(2)))
		self._off_tricount = cfo
		self.tricount, _ = bdat.read_builtin("u16", src, cfo, False, False)
		self._off_mtlinfo = off+4
		self.mtlinfo, _ = bdat.read_builtin("u16", src, off+4, False, False)
		self.texid = (vs.get_variable([self], "mtlinfo", 0, False)&(2047))
		self._off_meshnum = off+6
		self.meshnum, _ = bdat.read_builtin("u16", src, off+6, False, False)
		self._off_nextmeshoff = off+8
		self.nextmeshoff, _ = bdat.read_builtin("i32", src, off+8, False, False)
		vs.vars['origOff'] = off+0
		vs.vars['i'] = 0
		cfo = vs.get_variable([self], "ext1off", 0, False)
		self._off_ext1 = cfo
		self.ext1, _ = bdat.read_struct(meshext1, src, cfo, False, False, {})
		vs = ipvs
		if vs.get_variable([self], "nextmeshoff", 0, False) != 0:
			vs = fdvs
			vs.vars['origOff'] = off+0
			vs.vars['i'] = 0
			cfo = vs.get_variable([self], "nextmeshoff", 0, False)
			self._off_nextmesh = cfo
			self.nextmesh, _ = bdat.read_struct(mesh, src, cfo, False, False, {})
		else:
			self.nextmesh = None
		self._off_a = off+52
		self.a, _ = bdat.read_builtin("u16", src, off+52, False, False)
		self._off_b = off+54
		self.b, _ = bdat.read_builtin("u16", src, off+54, False, False)
		self._off_c = off+56
		self.c, _ = bdat.read_builtin("u16", src, off+56, False, False)
		self._off_color = off+64
		self.color, _ = bdat.read_builtin("u8", src, off+64, 3, False)
		self._off_numidxvals = off+72
		self.numidxvals, _ = bdat.read_builtin("i32", src, off+72, False, False)
		self._offend = TODO(size + sizeSrc)


class meshext1(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_unk1 = off
		self.unk1, off = bdat.read_builtin("i32", src, off, False, False)
		self._off_unkplane1 = off
		self.unkplane1, off = bdat.read_builtin("f32", src, off, 4, False)
		self._off_unkplane2 = off
		self.unkplane2, off = bdat.read_builtin("f32", src, off, 4, False)
		self._off_bbmax = off
		self.bbmax, off = bdat.read_builtin("f32", src, off, 3, False)
		self._off_bbmin = off
		self.bbmin, off = bdat.read_builtin("f32", src, off, 3, False)
		self._offend = off


class meshref(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_off = off+0
		self.off, _ = bdat.read_builtin("u32", src, off+0, False, False)
		vs = fdvs
		vs.vars['origOff'] = off+0
		vs.vars['i'] = 0
		cfo = vs.get_variable([self], "off", 0, False)
		self._off_mesh = cfo
		self.mesh, _ = bdat.read_struct(mesh, src, cfo, False, False, {})
		self._offend = TODO(size + sizeSrc)


class oct_1(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_a = off
		self.a, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_b = off
		self.b, off = bdat.read_builtin("f32", src, off, 4, False)
		self._off_c1 = off
		self.c1, off = bdat.read_builtin("f32", src, off, 2, False)
		self._off_c2 = off
		self.c2, off = bdat.read_builtin("u32", src, off, 2, False)
		self._off_d = off
		self.d, off = bdat.read_builtin("f32", src, off, 4, False)
		self._offend = off


class prm_hdr(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_u32_0 = off+0
		self.u32_0, _ = bdat.read_builtin("u32", src, off+0, 2, False)
		self._off_offmeshoffsets = off+8
		self.offmeshoffsets, _ = bdat.read_builtin("u32", src, off+8, False, False)
		self._off_meshcount = off+12
		self.meshcount, _ = bdat.read_builtin("u32", src, off+12, False, False)
		vs = fdvs
		vs.vars['origOff'] = off+0
		vs.vars['i'] = 0
		cfo = vs.get_variable([self], "offmeshoffsets", 0, False)
		self._off_meshoffsets = cfo
		self.meshoffsets, _ = bdat.read_builtin("u32", src, cfo, self.meshcount+0, False)
		vs = ipvs
		vs = fdvs
		vs.vars['origOff'] = off+0
		cfo = []
		for i in range(self.meshcount+0):
			vs.vars['i'] = i
			ceo = vs.get_variable([self], "meshoffsets", vs.get_variable([self], "i", 0, False), False)
			cfo.append(ceo)
		self._off_meshes = cfo
		self.meshes, _ = bdat.read_struct(mesh, src, cfo, self.meshcount+0, False, {})
		self._offend = TODO(size + sizeSrc)


class rm_3(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_unk1 = off
		self.unk1, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_b = off
		self.b, off = bdat.read_builtin("f32", src, off, 8, False)
		self._off_c1 = off
		self.c1, off = bdat.read_builtin("f32", src, off, 2, False)
		self._off_c2 = off
		self.c2, off = bdat.read_builtin("f32", src, off, 2, False)
		self._off_d1 = off
		self.d1, off = bdat.read_builtin("f32", src, off, 3, False)
		self._off_d2 = off
		self.d2, off = bdat.read_builtin("f32", src, off, 3, False)
		self._off_e = off
		self.e, off = bdat.read_builtin("f32", src, off, 2, False)
		self._offend = off


class tex(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_size = off
		self.size, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_fmt = off
		self.fmt, off = bdat.read_builtin("char", src, off, 4, False)
		self._off_fmt1 = off
		self.fmt1, off = bdat.read_builtin("char", src, off, 4, False)
		self._off_id = off
		self.id, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_height = off
		self.height, off = bdat.read_builtin("u16", src, off, False, False)
		self._off_width = off
		self.width, off = bdat.read_builtin("u16", src, off, False, False)
		self._off_nmips = off
		self.nmips, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_flags = off
		self.flags, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_unk2 = off
		self.unk2, off = bdat.read_builtin("u32", src, off, 2, False)
		self._off_text = off
		self.text, off = bdat.read_builtin("char", src, off, 128, True)
		self._off_datasize = off
		self.datasize, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_data = off
		self.data, off = bdat.read_builtin("u8", src, off, self.datasize+0, False)
		self._offend = off


class texgroup(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_count = off
		self.count, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_ids = off
		self.ids, off = bdat.read_builtin("u32", src, off, self.count+0, False)
		self._offend = off


class texhdr(bdat.Struct):
	def load(self):
		src = self._src
		off = self._off
		vs = ipvs = bdat.InParseVariableSource(self)
		fdvs = bdat.FullDataVariableSource(self)
		self._off_offtexoffsets = off
		self.offtexoffsets, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_offgrpoffsets = off
		self.offgrpoffsets, off = bdat.read_builtin("u32", src, off, False, False)
		self._off_num1 = off
		self.num1, off = bdat.read_builtin("i32", src, off, False, False)
		self._off_num2 = off
		self.num2, off = bdat.read_builtin("i32", src, off, False, False)
		vs = fdvs
		vs.vars['origOff'] = off
		vs.vars['i'] = 0
		cfo = vs.get_variable([self], "offtexoffsets", 0, False)
		self._off_texoffsets = cfo
		self.texoffsets, _ = bdat.read_builtin("u32", src, cfo, 2048, False)
		vs.vars['origOff'] = off
		vs.vars['i'] = 0
		cfo = vs.get_variable([self], "offgrpoffsets", 0, False)
		self._off_grpoffsets = cfo
		self.grpoffsets, _ = bdat.read_builtin("u32", src, cfo, 2048, False)
		vs.vars['origOff'] = off
		cfo = []
		for i in range(2048):
			vs.vars['i'] = i
			ceo = vs.get_variable([self], "texoffsets", vs.get_variable([self], "i", 0, False), False)
			vs.vars['off'] = ceo
			if vs.get_variable([self], "off", 0, False) == 0:
				ceo = None
			del vs.vars['off']
			cfo.append(ceo)
		self._off_textures = cfo
		self.textures, _ = bdat.read_struct(tex, src, cfo, 2048, False, {})
		vs.vars['origOff'] = off
		cfo = []
		for i in range(2048):
			vs.vars['i'] = i
			ceo = vs.get_variable([self], "grpoffsets", vs.get_variable([self], "i", 0, False), False)
			vs.vars['off'] = ceo
			if vs.get_variable([self], "off", 0, False) == 0:
				ceo = None
			del vs.vars['off']
			cfo.append(ceo)
		self._off_groups = cfo
		self.groups, _ = bdat.read_struct(texgroup, src, cfo, 2048, False, {})
		self._offend = off


