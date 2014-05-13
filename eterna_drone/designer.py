
import random

from eterna_drone.util import *
from eterna_drone.feature_generator_factory import *
from eterna_drone.construct_factory import *


def nupack_pair_score(c):

	f = open("test.in","w")
	f.write(c.sequence)
	f.close()

	subprocess.call("pairs test",shell=True)

	score =calculate_estimated_score(c.sequence,c.structure)

	return score 


class Designer(object):
	def __init__(self):
		data_path = os.environ["EternaDrone"]+"/eterna_drone/data/"
		self.bulge_type_count = pickle.load(open(data_path+"bulge_type_count_top.p","rb"))
		self.predictor = pickle.load( open( data_path+"predictor.p", "rb" ) )
		self.n_runs = 10
		#self.score_function = self.default_scoring_function
		self.score_function =nupack_pair_score


	def default_scoring_function(self,c):
		populate_features_for_constructs([c],self.feature_generators)

		data = []
		for f in self.features:
			data.append(c.features[f])

		predicted_scores = self.predictor.predict([data])

		return predicted_scores[0]

	def _setup(self,construct):
		count = 0
		while 1:
			for node in construct.ss_tree.nodes_to_optimize:
				if node.ss_type == "Basepair":
					self._mutate_basepair_node(node)

				elif node.ss_type == "Bulge":
					self._mutate_bulge_node(node,seq_max_pos=3)
			
				elif node.ss_type == "SingleStranded":
					self._mutate_single_strand_node(node)

			ss,seq = construct.ss_tree.get_ss_and_seq()

			if not self.exclude.search(seq[:58]):
				break

			count += 1

			if count > 10000:
				print "failed"
				return 

	def optimize_sequence(self,construct):
		self.allowed_bps = ['GC','CG','AU','UA']
		self.exclude = re.compile(r"(GGGG|AAAA|UUUU|CCCC)")

		self._setup(construct)

		ss,seq = construct.ss_tree.get_ss_and_seq()
		construct.sequence = seq

		self.feature_generators = FeatureGeneratorFactory.all_generators() 
		constructs = [construct]
		populate_features_for_constructs(constructs,self.feature_generators)

		self.features = constructs[0].features.keys()
		self.features.sort(reverse=True)


		best = self.score_function(construct,)
		best_seq = construct.sequence

		if len(construct.ss_tree.nodes_to_optimize) == 0:
			print best_seq,best
			sys.exit()

		for i in range(self.n_runs):

			rand = random.randrange(len(construct.ss_tree.nodes_to_optimize))
			rand_node = construct.ss_tree.nodes_to_optimize[rand]
			old_seq = None

			if rand_node.ss_type == "Basepair":
				old_seq = self._mutate_basepair_node(rand_node)

			elif rand_node.ss_type == "Bulge":
				old_seq = self._mutate_bulge_node(rand_node,seq_max_pos=10)
				
			elif rand_node.ss_type == "SingleStranded":
				old_seq = self._mutate_single_strand_node(rand_node)

			ss,seq = construct.ss_tree.get_ss_and_seq()


			if self.exclude.search(seq[:58]):
				rand_node.set_seq(old_seq)
				continue

			construct.sequence = seq

			score = self.score_function(construct)

			if score > best:
				best = score
				best_seq = seq

			else:
				rand_node.set_seq(old_seq)


		return best_seq,best



	def _mutate_basepair_node(self,node):
		capper = 0
		if node.parent != None:
			if node.parent.ss_type == "Bulge":
				capper = 1
		for child in node.children:
			if child.ss_type == "Bulge":
				capper = 1
				break 

		#only want GC or CG near bulges
		org_bp_str = node.bp_type
		bp_str = org_bp_str
		while bp_str == org_bp_str:
			if capper:
				bp_pos = random.randrange(0,2)
			else:
				bp_pos = random.randrange(0,4)
			bp_str = self.allowed_bps[bp_pos]
			node.set_seq(bp_str)

		return org_bp_str

	def _mutate_bulge_node(self,node,seq_max_pos=3):

		bulge_type = str(len(node.sx)) + "-" + str(len(node.sy))
		if bulge_type not in self.bulge_type_count:
			raise ValueError("unknown bulge type: "+ bulge_type)
		seq_counts = self.bulge_type_count[bulge_type]

		org_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)
		current_seq = org_seq
		while org_seq == current_seq:
			seq_pos = random.randrange(0,seq_max_pos)
			seq = seq_counts[seq_pos]
			node.set_seq(seq[0])
			current_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)

		return org_seq

	def _mutate_single_strand_node(self,node):

		node.revert_sequence()
		org_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)
		current_seq = org_seq
		for i in range(len(node.x_seq)):
			if node.x_seq[i] != "N":
				continue
			rand = random.randrange(1000)
			if rand > 800:
				node.x_seq[i] = "G"
			else:
				node.x_seq[i] = "A"
		for i in range(len(node.y_seq)):
			if node.y_seq[i] != "N":
				continue
			rand = random.randrange(1000)
			if rand > 800:
				node.y_seq[i] = "G"
			else:
				node.y_seq[i] = "A"
		#	org_seq = "".join(node.x_seq) + "-" + "".join(node.y_seq)
		#
		#	if org_seq == current_seq:
		#		node.revert_sequence()

		return org_seq

def main():
	ss  = "......((((((((((((((((((((((((....)))))))))))))))))))))))).....(((((((....)))))))....................."
	seq = "GGNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNAAAUAAAUUCGUUUAUUUAAAAGAAACAACAACAACAAC"
	c = Construct(seq=seq,ss=ss)
	designer = Designer()
	designer.optimize_sequence(c)




if __name__ == '__main__':
	main()


