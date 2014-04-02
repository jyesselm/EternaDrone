
import os 
import sys
import re
import glob
import argparse
import random

import matplotlib.pyplot as plt
from scipy.stats import *

from eterna_drone.util import *
from eterna_drone.feature_generator_factory import *

def parse_args():
	parser = argparse.ArgumentParser(
	    description='')
	#arguments for building in a structure if -s is set others are required
	parser.add_argument('-seq', help='sequence', required=False)
	parser.add_argument('-ss', help='secondary structure', required=False)

	args = parser.parse_args()
	return args

args = parse_args()
#check for valid arguments

data_path = os.environ["EternaDrone"]+"/eterna_drone/data/"
bulge_type_count = pickle.load(open(data_path+"bulge_type_count.p","rb"))
predictor = pickle.load( open( data_path+"predictor.p", "rb" ) )

construct = Construct(args.seq,args.ss,0)

#print len(construct.ss_tree.nodes_to_optimize)

allowed_bps = ['GC','CG','AU','UA']

for node in construct.ss_tree.nodes_to_optimize:
	if node.ss_type == "Basepair":
		capper = 0
		if node.parent != None:
			if node.parent.ss_type == "Bulge":
				capper = 1
		for child in node.children:
			if child.ss_type == "Bulge":
				capper = 1
				break

		#only want GC or CG near bulges
		if capper:
			bp_pos = random.randrange(0,2)
		else:
			bp_pos = random.randrange(0,4)
		bp_str = allowed_bps[bp_pos]
		node.res1 = bp_str[0]
		node.res2 = bp_str[1]
		node.bp_str = bp_str
	elif node.ss_type == "Bulge":
		bulge_type = str(len(node.sx)) + "-" + str(len(node.sy))
		if bulge_type not in bulge_type_count:
			raise ValueError("unknown bulge type: "+ bulge_type)
		seq_counts = bulge_type_count[bulge_type]
		seq_pos = random.randrange(0,3)
		seq = seq_counts[seq_pos]
		seqs = re.split("\-",seq[0])
		node.x_seq = list(seqs[0])
		if len(seqs) > 1: 
			node.y_seq = list(seqs[1])
	elif node.ss_type == "SingleStranded":
		node.revert_sequence()
		for i in range(len(node.x_seq)):
			if node.x_seq[i] != "N":
				continue
			rand = random.randrange(1000)
			if rand > 800:
				node.x_seq[i] = "G"
			else:
				node.x_seq[i] = "A"
		for i in range(len(node.y_seq)):
			if node.y_seq[i] != "N":
				continue
			rand = random.randrange(1000)
			if rand > 800:
				node.y_seq[i] = "G"
			else:
				node.y_seq[i] = "A"

ss,seq = construct.ss_tree.get_ss_and_seq()
print seq
construct.sequence = seq

feature_generators = FeatureGeneratorFactory.all_generators() 
constructs = [construct]
populate_features_for_constructs(constructs,feature_generators)

features = constructs[0].features.keys()
features.sort(reverse=True)

all_data = []
for c in constructs:
	data = []
	for f in features:
		data.append(c.features[f])
	all_data.append(data)

predicted_scores = predictor.predict(all_data)

print seq,ss,predicted_scores[0]





