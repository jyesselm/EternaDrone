
import os 
import sys
import re
import subprocess 

f = open("all_data.parsed")
lines = f.readlines()
f.close()


def get_free_energy_at_temp(temp):
	subprocess.call("RNAfold -T "+str(temp)+" -p2 -d2 < seq.fa > seq.out",shell=True)
	
	f = open("seq.out")
	seq_lines = f.readlines()
	f.close()

	ss_line = seq_lines[2]
	spl = re.split("\s+",ss_line)
	if len(spl) == 4:
		free_energy = spl[2][:-1]
	elif len(spl) == 3:
		free_energy = spl[1][1:-1]
	else:
		raise ValueError("not expected length")
	return float(free_energy)

sum = open("vienna_data.dat","w")

count = -1

for l in lines:
	count +=1 
	if count != 119:
		continue

	construct_spl = re.split("\s+",l)
	vienna_f = open("seq.fa","w")
	vienna_f.write(">seq1\n"+construct_spl[0])
	vienna_f.close()

	subprocess.call("RNAfold -T 37 -p2 -d2 < seq.fa > seq.out",shell=True)

	f = open("seq.out")
	seq_lines = f.readlines()
	f.close()

	ss_line = seq_lines[2]
	spl = re.split("\s+",ss_line)
	predicted_structure = spl[0]
	free_energy = spl[1][1:-1]
	#print predicted_structure,spl[1][1:-1]

	#print construct_spl[1]

	diff = 0.0
	for i,ss in enumerate(predicted_structure):
		if ss != construct_spl[1][i]:
			diff += 1

	spl = re.split("\s+",seq_lines[-1])

	done = 0
	current_temp = 130
	current = get_free_energy_at_temp(current_temp)
	melting_temp = -1
	while not done:
		if current != 0.0:
			#print "made it"
			#print current_temp,current
			closest = 10000
			closest_temp = 0
			for i in range(int(current_temp),int(last_temp),1):
				test = get_free_energy_at_temp(i)
				if abs(test) < abs(closest) and test != 0.0:
					closest = test
					closest_temp = i

			done = 1
			melting_temp = closest_temp
			#print closest,closest_temp

		last = current
		last_temp = current_temp

		current_temp -= 5
		current = get_free_energy_at_temp(current_temp)

	print diff/float(len(predicted_structure)),float(free_energy),melting_temp,float(spl[7][:-1]),float(spl[10])

	try:
		data = [diff/float(len(predicted_structure)),float(free_energy),melting_temp,float(spl[7][:-1]),float(spl[10])]
	except:
		continue

	data_str = " ".join([str(x) for x in data])

	sum.write(count + " " + data_str + "\n")

sum.close()













