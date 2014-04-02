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

from feature_generator import *

class FeatureGeneratorFactory(object):
	def __init__(self):
		pass

	#@staticmethod
	#def generators_from_file(file):
	
	@staticmethod
	def all_generators():
		generators = []
		generators.append(Sequence_FG())
		generators.append(Structure_FG())
		generators.append(Vienna_FG())

		return generators


