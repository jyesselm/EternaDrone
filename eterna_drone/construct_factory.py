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

import re
import random
import subprocess

from construct import *
from ss_tree import *

res = ['A','U','G','C']

def generate_bp(res1,res2):
	"""
	

	"""
	ss = ['(',')']
	seq = [res1,res2]
	bp = SSN_Basepair(ss,seq)
	return bp

def generate_hairpin_random(size):
	ss = []
	seq = []
	sx = []
	x_seq = []

	for i in range(size):
		sx.append(".")
		res_i = random.randrange(4)
		x_seq.append(res[res_i])

	ss.extend(sx)
	ss.extend(['(',')'])

	seq.extend(x_seq)
	seq.extend(['N','N'])

	return SSN_Bulge(ss,seq)

def generate_bulge_random(size_x,size_y):
	ss = []
	seq = []
	sx = []
	sy = []
	x_seq = []
	y_seq = []

	if size_x == 0 and size_y == 0:
		size_x += 1

	for i in range(size_x):
		sx.append(".")
		res_i = random.randrange(4)
		x_seq.append(res[res_i])

	for i in range(size_y):
		sy.append(".")
		res_i = random.randrange(4)
		y_seq.append(res[res_i])

	ss.extend(sx)
	ss.extend(['(',')'])
	ss.extend(sy)

	seq.extend(x_seq)
	seq.extend(['N','N'])
	seq.extend(y_seq)

	return SSN_Bulge(ss,seq)

def random_ss_node():
	rand = random.randrange(1000)

	node = None
	if rand < 850:
		res_i = random.randrange(4)
		res_j = random.randrange(4)
		node = generate_bp(res[res_i],res[res_j])
	else:
		x_size = random.randrange(5)
		y_size = random.randrange(5)
		node = generate_bulge_random(x_size,y_size)

	return node

def generate_random_rna(size):
	nodes = []
	for i in range(size):
		node = random_ss_node()

		if i == 0:
			nodes.append(node)
			continue

		nodes[-1].children.append(node)
		nodes.append(node)

	hairpin = generate_hairpin_random(random.randrange(3,7))
	nodes[-1].children.append(hairpin)

	return nodes[0].get_ss_and_seq()

def calculate_estimated_score(seq,ss):
	pairing_sum = {}

	f = open("test.ppairs")
	lines = f.readlines()
	f.close()

	lines = lines[15:]

	max = len(seq)

	for l in lines:
		spl = re.split("\s+",l)

		if int(spl[0]) > max or int(spl[1]) > max:
			continue

		if spl[0] not in pairing_sum:
			pairing_sum[spl[0]] = 0
		if spl[1] not in pairing_sum:
			pairing_sum[spl[1]] = 0

		pairing_sum[spl[0]] += float(spl[2])
		pairing_sum[spl[1]] += float(spl[2])

	score = 0
	points = 0.0

	for k,v in pairing_sum.iteritems():
		pos = int(k)-1

		paired = 1
		if ss[pos] == ".":
			paired = 0

		if paired == 0 and v < 0.10:
			points += 1
		if paired == 1 and v > 0.90:
			points += 1

	return (points / len(seq)) * 100


class ConstructFactory(object):

	@staticmethod
	def random():
		score = 100
		construct = None

		while score > 40:
			ss,seq = generate_random_rna(random.randrange(5,40))

			f = open("test.in","w")
			f.write(seq)
			f.close()

			subprocess.call("pairs test",shell=True)

			score = calculate_estimated_score(seq,ss)

			construct = Construct(seq,ss,score)

		return construct


		





