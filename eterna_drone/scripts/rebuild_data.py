# -*- coding: UTF-8 -*-

#	Copyright (C) 2013  Joseph Yesselman <jyesselm@stanford.edu>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os 
import sys
import re
import glob
import argparse
import random
from time import time

from eterna_drone.util import *
from eterna_drone.construct_factory import *
from eterna_drone.feature_generator_factory import *


def generated_simulated_construct_data(nconstructs,feature_generators,features):
	rand_constructs = []

	for i in range(nconstructs):
		r_construct = ConstructFactory.random()
		rand_constructs.append(r_construct)

	populate_features_for_constructs(rand_constructs,feature_generators)

	sim_data = []
	for c in rand_constructs:
		data = []
		for f in features:
			data.append(c.features[f])
		data.append(c.eterna_score)
		sim_data.append(data)

	pickle.dump(rand_constructs,open(data_path+"simulated_decoy_constructs.p","wb"))
	pickle.dump(sim_data,open(data_path+"simulated_decoy_data.p","wb"))

random.seed(time())
data_path = os.environ["EternaDrone"]+"/EternaDrone/data/"

#rebuild construct objects
rdat_files_path = os.environ["EternaDrone"]+"/EternaDrone/rdat_files"
constructs = get_constructs_from_rdats(dir=rdat_files_path)

#rebuild features
feature_generators = FeatureGeneratorFactory.all_generators() 
#populate_features_for_constructs(constructs,feature_generators)

constructs = pickle.load(open(data_path+"constructs.p","rb"))

#sorted feature list
features = constructs[0].features.keys()
features.sort(reverse=True)

#build simulated data for decoys in machine learning fit, need about 100
#decoys
generated_simulated_construct_data(101,feature_generators,features)

#extract just features and eterna score for machine learning fit
constructs_by_score = {}
bin = 5
for c in constructs:
	data = []
	for f in features:
		data.append(c.features[f])
	data.append(c.eterna_score)

	binned = round(float(c.eterna_score) / bin)*bin
	if binned not in constructs_by_score:
		constructs_by_score[binned] = []
	constructs_by_score[binned].append(data)

test_faction = 0.20
train_data = []
test_data = []

for k,v in constructs_by_score.iteritems():
	if int(k) == 0:
		continue

	cutoff = round(len(v)*test_faction)

	random.shuffle(v)

	for i,point in enumerate(v):
		if i < cutoff:
			test_data.append(point)
		else:
			train_data.append(point)

pickle.dump(train_data, open( data_path+"train_data.p", "wb" ))
pickle.dump(test_data, open( data_path+"test_data.p", "wb" ))
#pickle.dump(constructs,open(data_path+"constructs.p","wb"))




















