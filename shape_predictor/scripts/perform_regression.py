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

import sys
import cPickle as pickle

import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from scipy.stats import *

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

data_path = os.environ["ShapePredictor"]+"/shape_predictor/data/"

train_data = pickle.load( open( data_path+"train_data.p", "rb" ) )
decoy_data = pickle.load( open( data_path+"decoy_data.p", "rb" ) )
test_data = pickle.load(  open( data_path+"test_data.p", "rb" ) )

X = train_data
X.extend(decoy_data[:100])

y = []
for data in X:
	score = data.pop()
	y.append(score)

y = np.array(y)

clf = RandomForestRegressor(n_estimators=100)
clf.fit(X, y)

#save predictor to be used for later
pickle.dump(clf, open( data_path+"predictor.p", "wb" ))

#plot data
new_y= score_orig(X,clf)
plt.subplot(121)
plt.scatter(scores,new_y)

y_new = []

for e in new_y:
	y_new.append(e[0])

print "Correlation with training_data",pearsonr(scores,y_new)

x,y = score_all(test_data,clf)

y_new = []
for e in y:
	y_new.append(e[0])

plt.subplot(122)
plt.scatter(x,y_new)

print "Correlation with test_data",pearsonr(x,y_new)

plt.show()















