import numpy as np
import cPickle as pickle
import sys
import matplotlib.pyplot as plt
from scipy import stats

print(__doc__)

def score_all(train_data,svr):
	
	x = []
	y = []
	for data in train_data:
		if len(data) != 6:
			continue
		real = data.pop()
		predicted = svr.predict(data)
		x.append(real)
		y.append(predicted)
	return np.array(x),np.array(y)

def score_orig(train_data,svr):
	
	x = []
	y = []
	for data in train_data:
		predicted = svr.predict(data)
		y.append(predicted)
	return np.array(y)

###############################################################################
# Generate sample data

train_data = pickle.load( open( "train_data.p", "rb" ) )
test_data = pickle.load(  open( "test_data.p", "rb" ) )

print len(train_data)
X = train_data[::100]
print len(X)
y = []
scores = []
bin = 5
for data in X:
	score = data.pop()

	#binned = round (score / bin)
	#y.append(binned)
	scores.append(score)
y = np.array(scores)

###############################################################################

print stats.linregress(X, y)



sys.exit()

###############################################################################
# look at the results
import pylab as pl
pl.scatter(X, y, c='k', label='data')
pl.hold('on')
pl.plot(X, y_rbf, c='g', label='RBF model')
pl.plot(X, y_lin, c='r', label='Linear model')
pl.plot(X, y_poly, c='b', label='Polynomial model')
pl.xlabel('data')
pl.ylabel('target')
pl.title('Support Vector Regression')
pl.legend()
pl.show()
