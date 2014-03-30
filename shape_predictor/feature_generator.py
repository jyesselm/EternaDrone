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

import abc
import sys

from ss_tree import *
from util import *

class FeatureGenerator(object):
	"""
    Abstract Base class for feature generators, for inheritence only.
    """
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		return

	@abc.abstractmethod
	def generate_for_construct(self, construct):
		"""
		Each feature generator should have this function and will take a 
		construct object and populate its feature member with the features 
		that said generator creates.

		:param construct: the construct object to generate features for 
		:type construct: Construct Object

		"""
		return

class Sequence_FG(FeatureGenerator):
	"""
	Sequence dependent features.

	currently populates construct.features with 
	::
		percent_a
		percent_u
		percent_g
		percent_c
		max_a_repeat
		max_u_repeat
		max_g_repeat
		max_c_repeat

	"""
	def __init__(self):
		pass

	def _get_max_stretch(self,residue,sequence):
		max = 0
		count = 0
		for e in sequence:
			if e == residue:
				count += 1
			else:
				if count > max:
					max = count
				count =0

		return max

	def generate_for_construct(self,construct):
		a_content = 0.0
		u_content = 0.0
		g_content = 0.0
		c_content = 0.0

		sequence = construct.sequence

		for e in sequence:
			if e == "A":
				a_content += 1
			elif e == "U":
				u_content += 1
			elif e == "G":
				g_content += 1
			elif e == "C":
				c_content += 1
			else:
				raise ValueError("sequences can only have A,U,G,C not"+e)

		a_stretch = self._get_max_stretch("A",sequence)
		u_stretch = self._get_max_stretch("U",sequence)
		g_stretch = self._get_max_stretch("G",sequence)
		c_stretch = self._get_max_stretch("C",sequence)

		#update features
		construct.features['percent_a'] = a_content / len(sequence)
		construct.features['percent_u'] = u_content / len(sequence)
		construct.features['percent_g'] = g_content / len(sequence)
		construct.features['percent_c'] = c_content / len(sequence)
		construct.features['max_a_repeat'] = a_stretch
		construct.features['max_u_repeat'] = u_stretch
		construct.features['max_g_repeat'] = g_stretch
		construct.features['max_c_repeat'] = c_stretch

class Structure_FG(FeatureGenerator):
	"""
	Structure dependent features.

	currently populates construct.features with 
	::
		percent_au
		percent_gc
		percent_wc
		percent_nc
		n_basepairs
		not_capped_loops
		not_stem_capped
	"""	
	
	def __init__(self):
		pass

	def generate_for_construct(self, construct):
		au_pairs = 0.0
		gc_pairs = 0.0
		wc_pairs = 0.0
		nc_pairs = 0.0
		pairs = 0.0
		not_capped_loops = 0.0
		not_stem_capped = 0.0

		sstree = SecondaryStructureTree(construct.structure,construct.sequence)

		for bp in sstree.basepairs:
			bp_str = bp.bp_type
			if is_au(bp_str):	
				au_pairs += 1
				wc_pairs += 1
			elif is_gc(bp_str):
				gc_pairs += 1
				wc_pairs += 1
			else:
				nc_pairs += 1
			pairs += 1
			if bp.parent == None:
				if not is_gc(bp.bp_type):
					not_stem_capped += 1

		for bulge in sstree.bulges:
			children = bulge.children
			for child in children:
				if child.ss_type != "Basepair":
					continue
				if not is_gc(child.bp_type):
					not_capped_loops += 1	

			if bulge.parent == None:
				continue

			if bulge.parent.ss_type != "Basepair":
				#3way junctions
				continue
			if bulge.parent != None:
				if not is_gc(bulge.parent.bp_type):
					not_capped_loops += 1

		#update features
		#possibly seperate gu pairs out from nc?
		construct.features['percent_au'] = au_pairs / pairs
		construct.features['percent_gc'] = gc_pairs / pairs
		construct.features['percent_wc'] = wc_pairs / pairs
		construct.features['percent_nc'] = nc_pairs / pairs
		construct.features['n_basepairs'] = pairs
		construct.features['not_capped_loops'] = not_capped_loops
		construct.features['not_stem_capped'] = not_stem_capped

class Vienna_FG(FeatureGenerator):
	"""
	Vienna RNA feature.
	currently populates construct.features with
	::
		avg_structure_diff
		free_energy
		melting_temp
		mfe_prob
		ensemble_diversity
	"""
	def __init__(self):
		pass

	def generate_for_construct(self, construct):
		vienna_f = open("seq.fa","w")
		vienna_f.write(">seq1\n"+construct.sequence)
		vienna_f.close()

		subprocess.call("RNAfold -T 37 -p2 -d2 < seq.fa > seq.out",shell=True)

		f = open("seq.out")
		seq_lines = f.readlines()
		f.close()

		ss_line = seq_lines[2]
		spl = re.split("\s+",ss_line)
		predicted_structure = spl[0]
		free_energy = get_free_energy_at_temp(37)


		diff = 0.0
		for i,e in enumerate(predicted_structure):
			if e != construct.structure[i]:
				diff += 1

		spl = re.split("\s+",seq_lines[-1])

		done = 0
		current_temp = 130
		current = get_free_energy_at_temp(current_temp)
		melting_temp = -1
		while not done:
			if current != 0.0:
				#print "made it"
				#print current_temp,current
				closest = 10000
				closest_temp = 0
				for i in range(int(current_temp),int(last_temp),1):
					test = get_free_energy_at_temp(i)
					if abs(test) < abs(closest) and test != 0.0:
						closest = test
						closest_temp = i

				done = 1
				melting_temp = closest_temp
				#print closest,closest_temp

			last = current
			last_temp = current_temp

			current_temp -= 5
			current = get_free_energy_at_temp(current_temp)
			if current_temp == 0:
				melting_temp = 0
				break

		data = [diff/float(len(predicted_structure)),float(free_energy),melting_temp,float(spl[7][:-1]),float(spl[10])]
		
		construct.features['avg_structure_diff'] = diff/float(len(predicted_structure))
		construct.features['free_energy'] = float(free_energy)
		construct.features['melting_temp'] = melting_temp
		construct.features['mfe_prob'] = float(spl[7][:-1])
		construct.features['ensemble_diversity'] = float(spl[10])





















