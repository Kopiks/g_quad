


gq_in=open("prom_s.gff","r")
out_lib=open("out_lib","w+")
var_in=open("filtered_prom_s_var_raw.vcf", "r")

"""
Create a list for every item in input vcf file, info field converted into dictionary
"""
data=[]
for i, line in enumerate(var_in):				#for every line in input vcf file
	if not line.startswith("#"):				#ignore info lines
		line=line.split("\t")					#tab-delimited split
		info=line[7].split(";")					#;-delimited split of info field
		if info[0]=="INDEL": info[0]="INDEL=1"	#append = 1 to INDEL information to make it dictionary appropriate
		data.append(line[:7]+[dict(item.split("=") for item in info)])	#append a list of fields, with last one being dictionarized info's


for line in gq_in:
	print line
	line_s=line.split("\t")
	seq = list(line_s[8].split(";")[0].split("=")[1])
	seq_mut=seq[:]
	print "".join(seq)
	temp=[]
	out_seq=[]
	for record in data:
		if int(line_s[3]) <= int(record[1]) <= int(line_s[4]) and record[0]==line_s[0]:
			temp.append(record)
	if temp: print temp
	
	for n in temp:
		print n[7]["AN"]
		for m in range(int(n[7]["AN"])):
			if n[7]["AN"]==n[7]["AC"]:
				print int(n[1])-int(line_s[3])
				seq_mut[int(n[1])-int(line_s[3])]=n[4]
				print seq_mut
				print seq
				break
			else:
				ac_sum=0
				print n[7]["AC"].split(",")
				#ac_sum = ac_sum + k for k in n[7]["AC"].split(",")
				print ac_sum
				print sum(n[7]["AC"].split(","))
				if sum(n[7]["AC"].split(","))-int(n[7]["AN"])==0:
					pass
