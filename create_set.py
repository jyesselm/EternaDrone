
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

f = open("features.dat")
flines = f.readlines()
f.close()

v_hash = {}

for l in vlines:
	spl = re.split("\s+",l)
	spl.pop()
	num = spl.pop(0)
	v_hash[int(num)] = spl

f_hash = {}

for l in flines:
	spl = re.split("\s+",l)
	spl.pop()
	num = spl.pop(0)
	f_hash[int(num)] = spl


distro = {}
bin = 5

for i,l in enumerate(lines):
	spl = re.split("\s+",l)
	spl.pop()
	if i not in v_hash:
		continue

	v_data = v_hash[i]
	f_data = f_hash[i]
	f_data.insert(0,v_data[2])
	f_data.insert(0,v_data[1])
	f_data.append(v_data[0])
	f_data.append(v_data[3])
	f_data.append(v_data[4])

	f_data.append(spl[3])

	data = [float(x) for x in f_data]

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





















