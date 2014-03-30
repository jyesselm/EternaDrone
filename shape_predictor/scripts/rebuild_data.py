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

from shape_predictor.util import *
from shape_predictor.feature_generator_factory import *

def parse_args():
	parser = argparse.ArgumentParser(
	    description='')
	
	parser.add_argument('-s', help='pdb structure', required=False)

	args = parser.parse_args()
	return args

args = parse_args()

data_path = os.environ["ShapePredictor"]+"/shape_predictor/data/"

#rebuild construct objects
rdat_files_path = os.environ["ShapePredictor"]+"/shape_predictor/rdat_files"
constructs = get_constructs_from_rdats(dir=rdat_files_path)

#rebuild features
feature_generators = FeatureGeneratorFactory.all_generators() 

vienna_fg = Vienna_FG()

for c in constructs:
	for fg in feature_generators:
		fg.generate_for_construct(c)

pickle.dump(constructs,open(data_path+"constructs.p","wb"))




















