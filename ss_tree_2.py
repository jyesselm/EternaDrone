
import sys

class SecondaryStructureNode(object):

	def assign_children(self):

		if self.ss[0] == "(":

			pair = get_bracket_pair(0,self.ss)
			##print self.ss[0:pair+1]
			bp = Basepair(self.ss[0:pair+1],self.seq[0:pair+1],parent=self)
			self.children.append(bp)

			self.ss = self.ss[pair+2:]
			self.seq = self.seq[pair+2:]

		else:

			bulge = Bulge(self.ss,self.seq,parent=self)
			self.children.append(bulge)

			self.ss = []
			self.seq = []
		return 1

	def assign_all_children(self):

		##print self.ss
		while len(self.ss) > 0:
			self.assign_children()

class SingleStranded(SecondaryStructureNode):
	def __init__(self,seq,parent=None):
		self.seq = seq
		self.children = []
		self.ss_type = "SingleStranded"

class Basepair(SecondaryStructureNode):
	def __init__(self,ss,seq,parent=None):
		self.parent = parent
		self.children = []
		self.ss_type = "Basepair"
		self.seq = seq
		self.ss = ss

		self.res1 = self.seq.pop(0)
		self.res2 = self.seq.pop()
		self.bp_type = self.res1+self.res2

		self.ss.pop(0)
		self.ss.pop()

	def get_ss_and_seq(self):
		ss = ""
		seq = ""
		for c in self.children:
			c_ss,c_seq = c.get_ss_and_seq()
			ss += c_ss
			seq += c_seq

		return "(" + ss + ")", self.res1 + seq + self.res2

class Bulge(SecondaryStructureNode):
	def __init__(self,ss,seq,parent=None):
		self.parent = parent
		self.children = []
		self.ss_type = "Bulge"

		self.sx = []
		self.sy = []

		self.x_seq = []
		self.y_seq = []

		self.seq = seq
		self.ss = ss

		#print ss,seq

		#remove dots from start
		end = get_dot_bounds(0,self.ss)
		if end > -1 and self.ss[0] == ".":
			for i in range(end+1):
				self.sx.append(self.ss.pop(0))
				self.x_seq.append(self.seq.pop(0))

		end = get_dot_bounds(len(self.ss)-1,self.ss,reverse=1)
		diff = len(self.ss)-end
		#print "".join(self.ss),diff
		if diff > 0 and self.ss[-1] == ".":
			for i in range(diff):
				self.sy.append(self.ss.pop())
				self.y_seq.append(self.seq.pop())

		#print self.x_seq,self.y_seq

		#check for n junction
		#for e in ss:

	def get_ss_and_seq(self):
		ss = ""
		seq = ""
		for c in self.children:
			c_ss,c_seq = c.get_ss_and_seq()
			ss += c_ss
			seq += c_seq

		return  "".join(self.sx) + ss + "".join(self.sy), "".join(self.x_seq) + seq + "".join(self.y_seq)



class SecondaryStructureTree(object):
	def __init__(self,ss=None,seq=None):

		if ss == None:
			self.ss = []
			self.seq = []
			return

		self.ss = list(ss)
		self.seq = list(seq)
		self.nodes = []

		self.remove_ss_start()

		while len(self.ss) > 0:
			self.assign_structure()

		self.basepairs = []
		self.bulges = []

		for node in self.nodes:
			if node.ss_type == "Basepair":
				self.basepairs.append(node)
			elif node.ss_type == "Bulge":
				self.bulges.append(node)

	def remove_ss_start(self):

		if self.ss[0] == ".":
			end = get_dot_bounds(0,self.ss)
			ss = SingleStranded(self.seq[0:end+2])
			self.nodes.append(ss)
			for i in range(end+1):
				self.ss.pop(0)
				self.seq.pop(0)
			##print self.ss

		if self.ss[-1] == ".":
			end = get_dot_bounds(len(self.ss)-1,self.ss,reverse=1)
			ss = SingleStranded(self.seq[end-1:])
			self.nodes.append(ss)
			diff = len(self.ss)-end
			for i in range(diff):
				self.ss.pop()
				self.seq.pop()

	def assign_structure(self):

		node = None
		if self.ss[0] == "(":
			pair = get_bracket_pair(0,self.ss)
			node = Basepair(self.ss[0:pair+1],self.seq[0:pair+1])

			self.ss = self.ss[pair+1:]
			self.seq = self.seq[pair+1:]


		elif self.ss[0] == ".":	
			node = Bulge(self.ss,self.seq)
			self.ss = []
			self.seq = []


		open_nodes = [node]
		while len(open_nodes) > 0:
			current = open_nodes.pop()
			if current in self.nodes:
				continue
			self.nodes.append(current)
			current.assign_all_children()

			open_nodes.extend(current.children)

		
def get_bracket_pair(pos,ss):
	bracket_count = 0
	for i,e in enumerate(ss):
		if e == "(":
			bracket_count += 1
		elif e == ")":
			bracket_count -= 1
			if bracket_count == 0:
				return i
	raise ValueError("cannot find pair")

def get_dot_bounds(pos,ss,reverse=0):
	
	if not reverse:
		for i in range(pos+1,len(ss)):
			if ss[i] != ".":
				return i-1
		return len(ss)-1
	else:
		for i in range(pos-1,0,-1):
			if ss[i] != ".":
				return i+1
		return 0

	return pos

def is_au(bp_str):
	if bp_str == "AU" or bp_str == "UA":
		return 1
	else:
		return 0

def is_gc(bp_str):
	if bp_str == "GC" or bp_str == "CG":
		return 1
	else:
		return 0 

def is_wc(bp_str):
	if is_au(bp_str) or is_gc(bp_str):
		return 1
	else:
		return 0

def get_max_stretch(n,seq):

	max = 0
	count = 0
	for e in seq:
		if e == n:
			count += 1
		else:
			if count > max:
				max = count
			count =0

	return max







