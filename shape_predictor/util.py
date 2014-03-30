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
import subprocess
import cPickle as pickle

from rdatkit.datahandlers import RDATFile
from construct import *

def get_constructs_from_rdats(dir):
	"""
	using rdatkit parse all RDAT files in the directory specified and parse
	each construct's sequence, structure and score into construct objects.
	ONLY files with .rdat extension will be recognized as RDAT files other 
	files will be skipped

	:params dir: directory with rdat files 
	:type dir: str
	:returns: List of Construct Objects

	"""

	files = glob.glob(dir+"/*")
	rdat_files = []

	#make sure files are rdat files
	for file in files:
		if file[-4:] == "rdat":
			rdat_files.append(file)

	if len(rdat_files) == 0:
		raise ValueError("no rdat files in directory "+dir+" files must have rdat extension to be recognized")

	construct_objs = []
	mm = re.compile("Mutate and Map")

	for file in files:

		r = RDATFile()
		r.load(open(file))
		
		construct = r.constructs.values()
		constructs = construct[0].data

		for c in constructs:
			#some data entries dont have signal_to_noise variable, skip over 
			#them
			if 'signal_to_noise' not in c.annotations:
				continue
			data_quality = c.annotations['signal_to_noise']
			spl = re.split("\:",data_quality[0])

			#dont want to include weak data
			if spl[0] == "weak":
				continue

			name = c.annotations['MAPseq'][0]
			project_name = c.annotations['MAPseq'][1]

			#mutate and map data wont be useful since target structure is not 
			#correct with the mutation
			if mm.search(name) or mm.search(project_name):
				continue

			score = c.annotations['EteRNA'][0]
			spl1 = re.split("\:",score)

			c = Construct(seq=c.annotations['sequence'][0],ss=c.annotations['structure'][0],score=spl1[2])

			construct_objs.append(c)

	return construct_objs

#generally useful small functions
#basepair classifying functions
##############################################################################

def is_au(bp_str):
	"""
	does a simple string comparision to evaluate if this bp_str is an AU 
	basepair

	:params bp_str: the concatenation of both residue strings, AU or GC or CG etc 
	:type bp_str: str
	:returns: bool -- 1 if its an AU basepair 0 if not
	"""
	if bp_str == "AU" or bp_str == "UA":
		return 1
	else:
		return 0

def is_gc(bp_str):
	"""
	does a simple string comparision to evaluate if this bp_str is an GC 
	basepair

	:params bp_str: the concatenation of both residue strings, AU or GC or CG etc 
	:type bp_str: str
	:returns: bool -- 1 if its an GC basepair 0 if not
	"""

	if bp_str == "GC" or bp_str == "CG":
		return 1
	else:
		return 0 

def is_wc(bp_str):
	"""
	does a simple string comparision to evaluate if this bp_str is a watson-crick
	basepair

	:params bp_str: the concatenation of both residue strings, AU or GC or CG etc 
	:type bp_str: str
	:returns: bool -- 1 if its an watson-crick basepair 0 if not
	"""

	if is_au(bp_str) or is_gc(bp_str):
		return 1
	else:
		return 0

#vienna related functions
##############################################################################

def get_free_energy_at_temp(temp):
	subprocess.call("RNAfold -T "+str(temp)+" -p2 -d2 < seq.fa > seq.out",shell=True)
	
	f = open("seq.out")
	seq_lines = f.readlines()
	f.close()

	ss_line = seq_lines[2]
	spl = re.split("\s+",ss_line)
	if len(spl) == 4:
		free_energy = spl[2][:-1]
	elif len(spl) == 3:
		free_energy = spl[1][1:-1]
	else:
		raise ValueError("not expected length")
	return float(free_energy)












