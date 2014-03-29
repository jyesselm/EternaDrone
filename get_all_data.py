import os
import sys
import re
import subprocess
import cPickle as pickle

from ss_tree_2 import *

def get_features(sstree,sequence):
	au_pairs = 0
	gc_pairs = 0
	wc_pairs = 0
	nc_pairs = 0
	pairs = 0
	not_capped_loops = 0
	not_stem_capped = 0
	a = 0
	u = 0
	g = 0 
	c = 0
	a_stretch = get_max_stretch("A",sequence)
	u_stretch = get_max_stretch("U",sequence)
	g_stretch = get_max_stretch("G",sequence)
	c_stretch = get_max_stretch("C",sequence)

	for e in sequence:
		if e == "A":
			a += 1
		elif e == "U":
			u += 1
		elif e == "G":
			g += 1
		elif e == "C":
			c += 1
		else:
			print e			

	for bp in sstree.basepairs:
		bp_str = bp.bp_type
		
		if is_au(bp_str):	
			au_pairs += 1
			wc_pairs += 1
		elif is_gc(bp_str):
			gc_pairs += 1
			wc_pairs += 1
		else:
			nc_pairs += 1
		pairs += 1

	for bp in sstree.basepairs:
		if bp.parent == None:
			if not is_gc(bp.bp_type):
				not_stem_capped += 1

	for bulge in sstree.bulges:

		children = bulge.children
		for child in children:
			if child.ss_type != "Basepair":
				continue
			if not is_gc(child.bp_type):
				not_capped_loops += 1	

		if bulge.parent == None:
			continue

		if bulge.parent.ss_type != "Basepair":
			#3way junctions
			continue
		if bulge.parent != None:
			if not is_gc(bulge.parent.bp_type):
				not_capped_loops += 1

		string = str(float(au_pairs)/pairs) + " " + str(float(gc_pairs)/pairs) + " " + str(float(nc_pairs)/pairs)  + " " + str(float(a)/len(sequence)) + " " + str(float(u)/len(sequence)) + " " + str(float(g)/len(sequence)) + " " + str(float(c)/len(sequence)) + " " + str(pairs) + " " + str(not_stem_capped) + " " + str(not_capped_loops) +  " " + str(a_stretch) + " " + str(u_stretch) + " " + str(g_stretch) + " " + str(c_stretch)

		data = re.split("\s+",string)
		f_data = [float(x) for x in data]

		return f_data

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

def get_vienna_features(ss,seq):
	vienna_f = open("seq.fa","w")
	vienna_f.write(">seq1\n"+seq)
	vienna_f.close()

	subprocess.call("RNAfold -T 37 -p2 -d2 < seq.fa > seq.out",shell=True)

	f = open("seq.out")
	seq_lines = f.readlines()
	f.close()

	ss_line = seq_lines[2]
	spl = re.split("\s+",ss_line)
	predicted_structure = spl[0]
	free_energy = get_free_energy_at_temp(37)


	diff = 0.0
	for i,e in enumerate(predicted_structure):
		if e != ss[i]:
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
		if current_temp == 0:
			melting_temp = 0
			break

	#print diff/float(len(predicted_structure)),float(free_energy),melting_temp,float(spl[7][:-1]),float(spl[10])

	data = [diff/float(len(predicted_structure)),float(free_energy),melting_temp,float(spl[7][:-1]),float(spl[10])]

	return data

f = open("sim_data.dat")
lines = f.readlines()
f.close()

decoy_data = []

for l in lines:

	spl = re.split("\s+",l)

	sstree = SecondaryStructureTree(spl[0],spl[1])

	f_data = get_features(sstree,spl[1])
	v_data = get_vienna_features(spl[0],spl[1])

	f_data.insert(0,v_data[2])
	f_data.insert(0,v_data[1])
	f_data.append(v_data[0])
	f_data.append(v_data[3])
	f_data.append(v_data[4])
	f_data.append(spl[-2])

	data = [float(x) for x in f_data]

	decoy_data.append(data)


pickle.dump(decoy_data, open( "decoy_data.p", "wb" ))
