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

from construct import *
from ss_tree import *

res = ['A','U','G','C']

def generate_bp(res1,res2):
	"""
	

	"""
	ss = ['(',')']
	seq = [res1,res2]
	bp = Basepair(ss,seq)
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

	return Bulge(ss,seq)

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

	return Bulge(ss,seq)

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
		node = generate_bulge(x_size,y_size)

	return node


class ConstructFactory(object):

	@staticmethod
	def random(size):
		pass





