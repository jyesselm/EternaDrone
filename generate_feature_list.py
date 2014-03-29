
import sys
import re

from ss_tree_2 import *

def is_au(bp_str):
	if bp_str == "AU" or bp_str == "UA":
		return 1
	else:
		return 0

def is_gc(bp_str):
	if bp_str == "GC" or bp_str == "CG":
		return 1
	else:
		return 0 

def is_wc(bp_str):
	if is_au(bp_str) or is_gc(bp_str):
		return 1
	else:
		return 0

def get_max_stretch(n,seq):

	max = 0
	count = 0
	for e in seq:
		if e == n:
			count += 1
		else:
			if count > max:
				max = count
			count =0

	return max


f = open("all_data.parsed")
lines = f.readlines()
f.close()

f = open("features.dat","w")

count =0
for l in lines:

	spl = re.split("\s+",l)
	sequence = spl[0]
	ss = spl[1]

	#print sequence,ss

	sstree = SecondaryStructureTree(ss,sequence)

	#sys.exit()

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

		


	print count,au_pairs,gc_pairs,wc_pairs,nc_pairs,pairs,not_capped_loops,not_stem_capped,a,u,g,c,spl[-2]
	print count,a_stretch,u_stretch,g_stretch,c_stretch

	f.write(str(count) + " " + str(float(au_pairs)/pairs) + " " + str(float(gc_pairs)/pairs) + " " + str(float(nc_pairs)/pairs)  + " " + str(float(a)/len(sequence)) + " " + str(float(u)/len(sequence)) + " " + str(float(g)/len(sequence)) + " " + str(float(c)/len(sequence)) + " " + str(pairs) + " " + str(not_stem_capped) + " " + str(not_capped_loops) +  " " + str(a_stretch) + " " + str(u_stretch) + " " + str(g_stretch) + " " + str(c_stretch) + "\n")

	count += 1
















