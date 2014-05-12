
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

def mutate_basepair_node(node):
	capper = 0
	if node.parent != None:
		if node.parent.ss_type == "Bulge":
			capper = 1
	for child in node.children:
		if child.ss_type == "Bulge":
			capper = 1
			break

	#only want GC or CG near bulges
	org_bp_str = node.bp_type
	bp_str = org_bp_str
	while bp_str == org_bp_str:
		if capper:
			bp_pos = random.randrange(0,2)
		else:
			bp_pos = random.randrange(0,4)
		bp_str = allowed_bps[bp_pos]
		node.set_seq(bp_str)

	return org_bp_str

def mutate_bulge_node(node,seq_max_pos=3):

	bulge_type = str(len(node.sx)) + "-" + str(len(node.sy))
	if bulge_type not in bulge_type_count:
		raise ValueError("unknown bulge type: "+ bulge_type)
	seq_counts = bulge_type_count[bulge_type]

	org_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)
	current_seq = org_seq
	while org_seq == current_seq:
		seq_pos = random.randrange(0,seq_max_pos)
		seq = seq_counts[seq_pos]
		node.set_seq(seq[0])
		current_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)

	return org_seq

def mutate_single_strand_node(node):

	node.revert_sequence()
	org_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)
	current_seq = org_seq
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
	#	org_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)
	#
	#	if org_seq == current_seq:
	#		node.revert_sequence()

	return org_seq

args = parse_args()
#check for valid arguments

data_path = os.environ["EternaDrone"]+"/eterna_drone/data/"
bulge_type_count = pickle.load(open(data_path+"bulge_type_count.p","rb"))
predictor = pickle.load( open( data_path+"predictor.p", "rb" ) )

bulge_type = "4-0"

print bulge_type_count[bulge_type]


sys.exit()

construct = Construct(args.seq,args.ss,0)

allowed_bps = ['GC','CG','AU','UA']

for node in construct.ss_tree.nodes_to_optimize:
	if node.ss_type == "Basepair":
		mutate_basepair_node(node)

	elif node.ss_type == "Bulge":
		mutate_bulge_node(node,seq_max_pos=3)
		
	elif node.ss_type == "SingleStranded":
		mutate_single_strand_node(node)

ss,seq = construct.ss_tree.get_ss_and_seq()
construct.sequence = seq

feature_generators = FeatureGeneratorFactory.all_generators() 
constructs = [construct]
populate_features_for_constructs(constructs,feature_generators)

features = constructs[0].features.keys()
features.sort(reverse=True)

data = []
for f in features:
	data.append(construct.features[f])

predicted_scores = predictor.predict([data])

best = predicted_scores[0]
best_seq = construct.sequence

if len(construct.ss_tree.nodes_to_optimize) == 0:
	print best_seq,best
	sys.exit()

for i in range(100):

	rand = random.randrange(len(construct.ss_tree.nodes_to_optimize))
	rand_node = construct.ss_tree.nodes_to_optimize[rand]
	old_seq = None

	if rand_node.ss_type == "Basepair":
		old_seq = mutate_basepair_node(rand_node)

	elif rand_node.ss_type == "Bulge":
		old_seq = mutate_bulge_node(rand_node,seq_max_pos=10)
		
	elif rand_node.ss_type == "SingleStranded":
		old_seq = mutate_single_strand_node(rand_node)

	ss,seq = construct.ss_tree.get_ss_and_seq()
	construct.sequence = seq
	populate_features_for_constructs([construct],feature_generators)

	data = []
	for f in features:
		data.append(construct.features[f])

	predicted_scores = predictor.predict([data])

	if predicted_scores[0] > best:
		best = predicted_scores[0]
		best_seq = seq
	#	print best_seq,best

	else:
		rand_node.set_seq(old_seq)


print best_seq,best





