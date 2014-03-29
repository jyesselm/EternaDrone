from pyevolve import G1DList
from pyevolve import Mutators, Initializators
from pyevolve import GSimpleGA, Consts
import matplotlib.pyplot as plt
import math
import numpy as np

import cPickle as pickle


train_data = pickle.load( open( "train_data.p", "rb" ) )
test_data_set = pickle.load( open( "test_data.p", "rb" ) )

#print train_data[0]

#sys.exit()

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

		#if data[-1] < 85 and score > 95:
		#	total += 10000
		sum_x += data[-1]
		sum_y += score
		sum_xy += data[-1]*score
		sum_x2 += data[-1]**2
		sum_y2 += score**2

	#print sum_x,sum_y,sum_xy,sum_x2,sum_y2
	n = float(len(train_data))
	#try:
	r = (sum_xy - (sum_x*sum_y)/n) / math.sqrt((sum_x2 - ((sum_x**2)/n))*(sum_y2 - ((sum_y**2)/n)))
	#print r

	#except:
	#	r = 0


	return abs(r)
	#return total

def test_data(best,data_set):
	x = []
	y = []
	count = 0
	print best
	for data in data_set:
		score = 0
		for j,weight in enumerate(best):
			score += weight*data[j]
		x.append(data[-1])
		y.append(score)


		#if data[-1] > 99.9:
		#	print score,data[-1],data

	return np.array(x),np.array(y)

def run_main():
	genome = G1DList.G1DList(18)
	genome.setParams(rangemin=-30, rangemax=30, bestrawscore=0.00, rounddecimal=6)
	genome.initializator.set(Initializators.G1DListInitializatorReal)
	genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
	genome.evaluator.set(sphere)

	ga = GSimpleGA.GSimpleGA(genome)
	ga.setMinimax(Consts.minimaxType["maximize"])
	ga.setGenerations(20)
	ga.setMutationRate(0.06)
	ga.setCrossoverRate(0.9)
	ga.setPopulationSize(1000)
	ga.evolve(freq_stats=1)

	best = ga.bestIndividual()

	x,y = test_data(best,train_data)
	plt.subplot(211)
	plt.scatter(x,y)

	x,y = test_data(best,test_data_set)
	plt.subplot(212)
	plt.scatter(x,y)

	plt.show()

	print best

if __name__ == "__main__":
	run_main()

#0.42297746009171167, 0.2128809709617746, 20, -14.985764983563591, -3.0473025072441073, 11.490538826148345, 8.834881360160743, 10.63346432024519, 17.339805597017246, -2.5500442039956024, -6.582751961185492, -16.86940139455162, -1.7627322604728803, -10.813001152714454, -7.577030784515877, -1.028994259436117, 7.285740254350426, 19.682380450367674


