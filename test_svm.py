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
decoy_data = pickle.load( open( "decoy_data.p", "rb" ) )
test_data = pickle.load(  open( "test_data.p", "rb" ) )

"""for data in test_data:
	for data2 in train_data:
		if data[0] == data2[0] and data[1] == data2[1] and data[2] == data2[2]:
			print data,data2
			sys.exit()

sys.exit()
"""

print len(train_data)
X = train_data
X.extend(decoy_data[:100])
print len(X)
y = []
scores = []
bin = 10
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
from sklearn.ensemble import RandomForestRegressor

clf = RandomForestRegressor(n_estimators=100)
clf.fit(X, scores)

pickle.dump(clf, open( "predictor.p", "wb" ))

#clf = linear_model.LinearRegression()
#clf.fit(X,y)

#svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
#svr_lin = SVR(kernel='linear', C=1e3)
#svr_poly = SVR(kernel='poly', C=1e3, degree=2)
#y_rbf = svr_rbf.fit(X, scores).predict(X)
#y_lin = svr_lin.fit(X, y).predict(X)
#y_poly = svr_poly.fit(X, y).predict(X)

#print X

new_y= score_orig(X,clf)
plt.subplot(121)
plt.scatter(scores,new_y)

y_new = []

for e in new_y:
	y_new.append(e[0])

print pearsonr(scores,y_new)


x,y = score_all(test_data,clf)

y_new = []

for e in y:
	y_new.append(e[0])

plt.subplot(122)
plt.scatter(x,y_new)

print pearsonr(x,y_new)


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
