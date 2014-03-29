from scipy.stats import *
import matplotlib.pyplot as plt
import numpy as np
import re 
import sys

f = open(sys.argv[1])
lines = f.readlines()
f.close()

x = []
y = []

avg_diff = 0

for l in lines:
	spl = re.split("\s+",l)
	x.append(float(spl[0]))
	y.append(float(spl[1]))
	avg_diff += abs(float(spl[0]) - float(spl[1]))

x = np.array(x)
y = np.array(y)

plt.subplot(111)
plt.scatter(x,y)

print pearsonr(x,y)
print avg_diff / len(x)
plt.show()
