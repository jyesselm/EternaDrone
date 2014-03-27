
import os 
import sys
import re
import cPickle as pickle
import random

f = open("all_data.parsed")
lines = f.readlines()
f.close()

f = open("vienna_data.dat")
vlines = f.readlines()
f.close()

v_hash = {}

for l in vlines:
	spl = re.split("\s+",l)
	spl.pop()
	num = spl.pop(0)
	v_hash[int(num)] = spl


distro = {}
bin = 5

for i,l in enumerate(lines):
	spl = re.split("\s+",l)
	spl.pop()
	if i not in v_hash:
		continue

	v_data = v_hash[i]
	v_data.append(spl[3])

	data = [float(x) for x in v_data]

	data[0] *= 100
	data[1] /= len(spl[0])
	data[1] *= 100
	data[2] /= len(spl[0])
	data[2] *= 100

	binned = round(float(data[-1]) / bin)*bin
	if binned not in distro:
		distro[binned] = []
	distro[binned].append(data)

#for k,v in distro.iteritems():
#	print k,len(v)

test_faction = 0.20

train_data = []
test_data = []

for k,v in distro.iteritems():
	if int(k) == 0:
		continue

	cutoff = round(len(v)*test_faction)

	random.shuffle(v)

	for i,point in enumerate(v):
		if i < cutoff:
			test_data.append(point)
		else:
			train_data.append(point)

#print len(test_data),len(train_data)

pickle.dump(train_data, open( "train_data.p", "wb" ))
pickle.dump(test_data, open( "test_data.p", "wb" ))





















