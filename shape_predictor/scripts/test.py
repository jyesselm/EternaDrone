
import os 
import sys
import re
import glob
import argparse

from shape_predictor.util import *

data_path = os.environ["ShapePredictor"]+"/shape_predictor/data/"
constructs = pickle.load(open(data_path+"constructs.p","rb"))

#print constructs[0]

def add(a,b):
	return a+b

construct = constructs[0]

code_str = """
test = melting_temp + percent_u*percent_g
"""

features = construct.features.keys()

for f in features:
	real_f = "construct.features[\'"+f+"\']"
	code_str = code_str.replace(f,real_f)

code_obj = compile(code_str, '<string>', 'single')


exec code_obj
print test