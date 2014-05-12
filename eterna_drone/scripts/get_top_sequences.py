
import sys
import re
import cPickle as pickle

from redesign.varna import *

from eterna_drone.construct import *

def generate_bulge_type_data():
	count = 0
	bulge_type = {}

	for c in constructs:

		if c.eterna_score < 90:
			continue

		ss_tree = SecondaryStructureTree(c.structure,c.sequence)

		n_ways = []
		hairpins = []
		two_ways = []
		seen = []

		for n in ss_tree.bulges:
			if len(n.children) > 1:
				n_ways.append(n)
			elif len(n.children) == 1:
				two_ways.append(n)
			elif len(n.children) == 0:
				hairpins.append(n)
			else:
				raise ValueError("unexpected condition")

		for n_way in n_ways:
			sequences = []
			bp_children = []
			for child in n_way.children:
				if child.ss_type == "Bulge":
					seen.append(child)
					sequence = "".join(child.x_seq) + "".join(child.y_seq)
					sequences.append(sequence)

			seq = "".join(n_way.x_seq) + "-"
			key = str(len(n_way.x_seq)) + "-"
			for s in sequences:
				seq += s + "-"
				key += str(len(s)) + "-"
			seq = "".join(n_way.y_seq) 
			key += str(len(n_way.y_seq))

			if key not in bulge_type:
				bulge_type[key] = []

			bulge_type[key].append(seq)

		for n in hairpins:
			if n in seen:
				continue

			length = 0
			sequence = None
			if len(n.x_seq) > len(n.y_seq):
				length = len(n.x_seq)
				sequence = "".join(n.x_seq)
			else:
				length = len(n.y_seq)
				sequence = "".join(n.y_seq)

			if length not in bulge_type:
				bulge_type[length] = []


			bulge_type[length].append(sequence)

		for n in two_ways:
			if n in seen:
				continue

			key = str(len(n.x_seq)) + "-" + str(len(n.y_seq))
			seq = "".join(n.x_seq) + "-" + "".join(n.y_seq)

			if key not in bulge_type:
				bulge_type[key] = []

			bulge_type[key].append(seq)

		count += 1

	pickle.dump(bulge_type,open(data_path+"bulge_types_top.p","wb"))	

def generate_bulge_type_count():
	bulge_type = pickle.load(open(data_path+"bulge_types_top.p","rb"))

	bulge_type_count = {}

	for k,v in bulge_type.iteritems():
		count = {}
		for seq in v:
			if seq not in count:
				count[seq] = 0
			count[seq] += 1

		count_array = count.items()
		count_array = sorted(count_array, key= lambda x : x[1], reverse=True)

		bulge_type_count[k] = count_array

	pickle.dump(bulge_type_count, open(data_path+"bulge_type_count_top.p","wb"))


data_path = os.environ["EternaDrone"]+"/eterna_drone/data/"
constructs = pickle.load(open(data_path+"constructs.p","rb"))

generate_bulge_type_data()
generate_bulge_type_count()

sys.exit()

bulge_type_count = pickle.load(open(data_path+"bulge_type_count.p","rb"))

varna = Varna()


for k,v in bulge_type_count.iteritems():

	spl = re.split("\-", str(k))

	#hairpin
	if len(spl) == 1:
		continue
		f = open(str(k)+".dat","w")

		for seq_info in v:
			seq,count = seq_info
			final_seq = "GC" + seq + "CG"
			final_ss  = "(("

			for i in range(len(seq)):
				final_ss += "."

			final_ss += "))"

			print final_seq
			print final_ss

			f.write(seq + " " + str(count) + "\n")

			varna.new_image_by_str(str(k)+"-"+seq+".svg",final_ss,final_seq)

	#if 


	#sys.exit()