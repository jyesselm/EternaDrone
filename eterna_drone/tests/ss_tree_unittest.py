import os
import unittest
import sys

import cPickle as pickle

from eterna_drone.construct import *

class SecondaryStructureTreeUnittest(unittest.TestCase):

	def setUp(self):
		data_path = os.environ["EternaDrone"]+"/eterna_drone/data/"
		self.constructs = pickle.load(open(data_path+"constructs.p","rb"))

	def test_rebuild_ss_and_seq(self):
		for i,c in enumerate(self.constructs):
			ss_tree = SecondaryStructureTree(c.structure,c.sequence)

			nss,nseq = ss_tree.get_ss_and_seq()

			if nss != c.structure or nseq != c.sequence:
				print c.structure
				print nss
				print c.sequence
				print nseq
				self.fail("failed on construct " + str(i))




def main():
    unittest.main()

if __name__ == '__main__':
    main()




