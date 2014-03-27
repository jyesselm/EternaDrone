from pyevolve import G1DList
from pyevolve import Mutators, Initializators
from pyevolve import GSimpleGA, Consts
import matplotlib.pyplot as plt
import numpy as np
import math

import cPickle as pickle


train_data = pickle.load( open( "train_data.p", "rb" ) )

# This is the Sphere Function
def sphere(xlist):
	total = 0
	sum_x = 0
	sum_y = 0
	sum_xy = 0
	sum_x2 = 0
	sum_y2 = 0
	for data in train_data:
		score = 0
		for j,weight in enumerate(xlist):
			score += weight*data[j]
		#total += abs(score - data[-1])**2
		sum_x += data[-1]
		sum_y += score
		sum_xy += data[-1]*score
		sum_x2 += data[-1]**2
		sum_y2 += score**2

	n = float(len(train_data))


	#print sum_x,sum_y,sum_xy,sum_x2,sum_y2
	try:
		r = (sum_xy - (sum_x*sum_y)/n) / math.sqrt((sum_x2 - ((sum_x**2)/n))*(sum_y2 - ((sum_y**2)/n)))
	except:
		r = 0

	return abs(r)

def test_data(best):
	x = []
	y = []
	count = 0
	print best
	for data in train_data:
		score = 0
		for j,weight in enumerate(best):
			score += weight*data[j]
		x.append(data[-1])
		y.append(score)


		#if data[-1] > 99.9:
		#	print score,data[-1],data

	return np.array(x),np.array(y)

def run_main():
	genome = G1DList.G1DList(5)
	genome.setParams(rangemin=0, rangemax=30, bestrawscore=0.00, rounddecimal=6)
	genome.initializator.set(Initializators.G1DListInitializatorReal)
	genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
	genome.evaluator.set(sphere)

	ga = GSimpleGA.GSimpleGA(genome)
	ga.setMinimax(Consts.minimaxType["maximize"])
	ga.setGenerations(20)
	ga.setMutationRate(0.06)
	ga.setCrossoverRate(0.9)
	ga.setPopulationSize(200)
	ga.evolve(freq_stats=1)

	best = ga.bestIndividual()

	x,y = test_data(best)

	plt.subplot(111)
	plt.scatter(x,y)
	plt.show()

	print best

if __name__ == "__main__":
	run_main()



