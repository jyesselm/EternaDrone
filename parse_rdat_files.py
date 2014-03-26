
import os 
import sys
import re
import glob


from rdatkit.datahandlers import RDATFile

files =glob.glob("rdat_files/*")

f = open("all_data.parsed","w")

mm = re.compile("Mutate and Map")

distro = {}
bin = 10

for file in files: 

	r = RDATFile()
	r.load(open(file))

	construct = r.constructs.values()
	constructs = construct[0].data

	count = 0

	for c in constructs:
		if 'signal_to_noise' not in c.annotations:
			continue
		data_quality = c.annotations['signal_to_noise']
		spl = re.split("\:",data_quality[0])

		if spl[0] == "weak":
			continue

		name = c.annotations['MAPseq'][0]
		project_name = c.annotations['MAPseq'][1]

		if mm.search(name) or mm.search(project_name):
			print name,project_name
			continue

		score = c.annotations['EteRNA'][0]
		spl1 = re.split("\:",score)

		f.write(c.annotations['sequence'][0] + " " + c.annotations['structure'][0] + " " + spl[0] + " " + spl1[2] + "\n")

		binned = round(float(spl1[2]) / bin)*bin
		if binned not in distro:
			distro[binned] = 0
		distro[binned] += 1

		#print c.annotations['sequence'][0],c.annotations['structure'][0],c.annotations['EteRNA'][0]
		count += 1

f.close()

for k,v in distro.iteritems():
	print k,v

print count
#print constructs[0].annotations

#values = r.values['Motif Assembled GAAA tetraloop binders']
