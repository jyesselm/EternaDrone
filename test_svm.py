import numpy as np
import cPickle as pickle
import sys
import matplotlib.pyplot as plt

print(__doc__)

def score_all(train_data,svr):
	
	x = []
	y = []
	for data in train_data:
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
X = train_data
print len(X)
y = []
scores = []
bin = 5
for data in X:
	score = data.pop()

	binned = round (score / bin)
	y.append(binned)
	scores.append(score)
y = np.array(y)

###############################################################################
# Fit regression model
from sklearn import svm
from sklearn import linear_model
from scipy.stats import *

clf = linear_model.LinearRegression()
clf.fit(X,y)

#svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
#svr_lin = SVR(kernel='linear', C=1e3)
#svr_poly = SVR(kernel='poly', C=1e3, degree=2)
#y_rbf = svr_rbf.fit(X, y).predict(X)
#y_lin = svr_lin.fit(X, y).predict(X)
#y_poly = svr_poly.fit(X, y).predict(X)

#print X

new_y= score_orig(X,clf)
plt.subplot(121)
plt.scatter(scores,new_y)

print pearsonr(scores,new_y)

x,y = score_all(test_data,clf)

plt.subplot(122)
plt.scatter(x,y)

print pearsonr(x,y)


plt.show()


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
