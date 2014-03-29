class SecondaryStructureElement(object):
	def add_child(self,child):
		self.children.append(child)

	def remove_child(self,rchild):
		id = 0
		for i,child in enumerate(self.children):
			if child == rchild:
				id = i
		self.children.pop(id)

	def equal(self,sse):
		if self.pos1 == sse.pos1 and self.pos2 == sse.pos2:
			return 1
		else:
			return 0

class Basepair(SecondaryStructureElement):
	def __init__(self,pos1,pos2,parent=None):
		self.parent = parent
		self.children = []
		self.pos1 = pos1
		self.pos2 = pos2
		self.res1 = "N"
		self.res2 = "N"
		self.type = "Basepair"
		self.string = ""

	def copy(self):
		copy = Basepair(self.pos1,self.pos2)
		copy.res1 = self.res1
		copy.res2 = self.res2
		for child in self.children:
			copied_child = child.copy()
			copied_child.parent = copy
			copy.add_child(copied_child)
		return copy

	def to_string(self):
		string = ""
		sorted_childen = sorted(self.children,key=lambda x: x.pos1)
		for child in sorted_childen:
			string += child.to_string()
		return "(" + string + ")"

	def get_sequence(self):
		string = ""
		sorted_childen = sorted(self.children,key=lambda x: x.pos1)
		for child in sorted_childen:
			string += child.get_sequence()
		return self.res1 + string + self.res2

class Bulge(SecondaryStructureElement):
	def __init__(self,pos1,pos2,sx,sy,parent=None):
		self.parent = parent
		self.children = []
		self.pos1 = pos1
		self.pos2 = pos2
		self.sx = sx
		self.sy = sy
		self.type = "Bulge"
		self.string = ""

		self.sx_res = []
		self.sy_res = []
		for x in range(sx):
			self.sx_res.append("N")
		for x in range(sy):
			self.sy_res.append("N")

	def copy(self):
		copy = Bulge(self.pos1,self.pos2,self.sx,self.sy,parent=self.parent)
		for child in self.children:
			copy.add_child(child.copy())
		return copy

	def to_string(self):
		string = ""
		sorted_childen = sorted(self.children,key=lambda x: x.pos1)
		for child in sorted_childen:
			string += child.to_string()
		sx_string = ""
		sy_string = ""
		if string == "":
			for x in range(self.sx):
				sx_string += "."
			return sx_string
		for x in range(self.sx):
				sx_string += "."
		for x in range(self.sy):
			sy_string += "."
		return sx_string + string + sy_string

	def get_sequence(self):
		string = ""
		sorted_childen = sorted(self.children,key=lambda x: x.pos1)
		for child in sorted_childen:
			string += child.get_sequence()
		if string == "":
			return "".join(self.sx_res)
		return "".join(self.sx_res) + string + "".join(self.sy_res)

class SecondaryStructureTree(object):
	def __init__(self,ss,seq):
		SSEs = []

		pos = 0

		print ss,seq


		seen_bulge = {}
		seq_array = seq

		while (pos < len(ss)):
			if ss[pos] == "(":
				pos2 = find_other_res_in_bp(pos,ss)
				sse = Basepair(pos,pos2)
				sse.res1 = seq_array[pos]
				sse.res2 = seq_array[pos2]
				parent = find_parent_sse(sse)
				if parent != None:
					sse.parent = parent
					parent.add_child(sse)
				SSEs.append(sse)

			if ss[pos] == "." and pos not in seen_bulge:
				parent = find_parent_sse_by_pos(pos,SSEs)
				bulged_residues_sx = 0
				bulged_residues_sy = 0
				sx_res = []
				sy_res = []
				pos1 = -1
				pos2 = -1
				for i in range(pos,len(ss)):
					if ss[i] == ".":
						bulged_residues_sx += 1
						sx_res.append(seq_array[i])
						pos1 = i
					else:
						break
				if parent == None:
					parent = find_parent_sse_by_pos_2(pos1,SSEs)
				if parent == None:
					parent = find_parent_sse_by_pos_2(find_other_res_in_bp(pos+1,ss)-1,SSEs)
				if parent == None:
					print "error",pos+1,pos1+1
					sys.exit()
				for j in range(parent.pos2-1,0,-1):
					if ss[j] == ".":
						bulged_residues_sy += 1
						sy_res.append(seq_array[j])
						seen_bulge[j] = 1
						pos2 = j
					else:
						break

				if pos2 == -1:
					pos2 = pos1
				sse = Bulge(pos1,pos2,bulged_residues_sx,bulged_residues_sy,parent=parent)
				sse.sx_res = sx_res
				sse.sy_res = sy_res
				parent.add_child(sse)

				SSEs.append(sse)
				pos = pos1
				
			pos+=1

		print SSEs

def find_parent_sse(SSE):
	parent = None
	for previous_SSE in SSEs:
		if previous_SSE.pos1 == SSE.pos1-1:
			parent = previous_SSE 
		elif previous_SSE.pos2 == SSE.pos2+1:
			parent = previous_SSE 
	return parent

def find_parent_sse_by_pos(pos,SSEs):
	parent = None
	for previous_SSE in SSEs:
		if previous_SSE.pos1 == pos-1:
			parent = previous_SSE 
	return parent

def find_parent_sse_by_pos_2(pos,SSEs):
	parent = None
	for previous_SSE in SSEs:
		if previous_SSE.pos2 == pos+1:
			parent = previous_SSE 
	return parent

def gather_sses(head):
	seen_sses = {}
	sses = []
	opened = [head]
	while len(opened) > 0:
		current = opened.pop(0)
		sses.append(current)
		seen_sses[current] = 1
		for child in current.children:
			if child in seen_sses:
				continue
			opened.append(child)
	return sses

def find_other_res_in_bp(pos,ss):
	parth_count = 1
	for i in range(pos+1,len(ss)):
		if ss[i] == "(":
			parth_count += 1
		if ss[i] == ")":
			parth_count -= 1
			if parth_count == 0:
				return i
	raise ValueError("could not find the paired ) where the ( is at "+str(pos))


