
import os 
import sys
import re
import glob
import argparse

import matplotlib.pyplot as plt
from scipy.stats import *

from shape_predictor.util import *
from shape_predictor.feature_generator_factory import *

def parse_args():
	parser = argparse.ArgumentParser(
	    description='')
	#arguments for building in a structure if -s is set others are required
	parser.add_argument('-seq', help='sequence', required=False)
	parser.add_argument('-ss', help='secondary structure', required=False)
	parser.add_argument('-f', help='file', required=False)
	parser.add_argument("-model", help='user specified model',required=False)

	args = parser.parse_args()
	return args

def parse_model_file(file,features):
	try:
		f = open(file)
		lines = f.readlines()
		f.close()
	except IOError:
		raise IOError("model file="+file+" does not exists please check the path\n") 	
	functions = []

	for l in lines:
		if len(l) < 2:
			continue
		#skip comments
		if l[0] == "#":
			continue
		#catch blank lines, python sometimes angers me
		spl = re.split("\s+",l)
		count = 0
		for e in spl:
			if e != '':
				count += 1

		if count == 0:
			continue

		code_str = l.rstrip()

		for f in features:
			real_f = "construct.features[\'"+f+"\']"

			if re.findall("([^\'])"+f,code_str):
				groups = re.findall("([^\'])"+f,code_str)
				for extra_char in groups:
					code_str = re.sub("\\"+extra_char+f, extra_char+real_f, code_str)

		functions.append(code_str)

	full_code_str = "score = " + " + ".join(functions)
	code_obj = compile(full_code_str, '<string>', 'single')
	return code_obj

args = parse_args()
#check for valid arguments

#get constructs
data_path = os.environ["ShapePredictor"]+"/shape_predictor/data/"
constructs = pickle.load(open(data_path+"constructs.p","rb"))
features = constructs[0].features.keys()
features.sort(key = lambda x : len(x), reverse=True)

model = None

if args.model:
	model = parse_model_file(args.model,features)

precompiled_data = 0

if args.seq and args.ss:
	construct = Construct(args.seq,args.ss,0)
	feature_generators = FeatureGeneratorFactory.all_generators() 

	constructs = [construct]
	populate_features_for_constructs(constructs,feature_generators)

elif args.f:
	raise ValueError("not implemented yet")

else:
	print "no new sequences and structures are specified using precompiled constructs"
	precompiled_data = 1

real_scores = []
predicted_scores = []
if model:

	for c in constructs:
		#set the correct local variable name for the compiled code object
		construct = c
		exec model
		real_scores.append(float(c.eterna_score))
		#local variable score gets set by exec model, see parse_model_file
		predicted_scores.append(score)
else:
	#get features
	features = constructs[0].features.keys()
	features.sort(reverse=True)

	real_scores = []
	all_data = []
	for c in constructs:
		data = []
		for f in features:
			data.append(c.features[f])
		real_scores.append(float(c.eterna_score))
		all_data.append(data)

	predictor = pickle.load( open( data_path+"predictor.p", "rb" ) )
	predicted_scores = predictor.predict(all_data)

if precompiled_data:
	print "Correlation with eterna score",pearsonr(real_scores,predicted_scores)
	sys.exit(0)

for i,c in enumerate(constructs):
	print c.sequence,c.structure,predicted_scores[i]





