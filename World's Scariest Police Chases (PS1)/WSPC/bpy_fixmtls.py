import bpy 

for obj in bpy.data.objects:
	for slots in obj.material_slots:
		slots.material.alpha_threshold = 0
		slots.material.blend_method = "CLIP"
		NT = slots.material.node_tree
		for node in NT.nodes:
			#print(node.type)
			if node.type == "TEX_IMAGE":
				node.interpolation = "Closest"
			elif node.type == "BSDF_PRINCIPLED":
				for ni in node.inputs:
					if ni.name != "Base Color": continue
					tex = [link.from_socket.node for link in NT.links if link.to_socket == ni][0]
					if tex.type != "TEX_IMAGE": break
					#print("INPUT")
					#print(["%s=%s" % (k, getattr(ni, k)) for k in dir(ni)])
					attr = NT.nodes.new("ShaderNodeAttribute")
					attr.attribute_name = "Col"
					mix = NT.nodes.new("ShaderNodeMixRGB")
					mix.blend_type = "MULTIPLY"
					mix.inputs[0].default_value = 1
					NT.links.new(mix.outputs[0], ni)
					NT.links.new(attr.outputs[0], mix.inputs[1])
					NT.links.new(tex.outputs[0], mix.inputs[2])
					break
			else:
				pass#print(["%s=%s" % (k, getattr(node, k)) for k in dir(node)])
