#extract "perfect" Gqs -> score == 0 in gff file

inp = open("The_list.gff","r")
out = open("Perfect.gff","w")
for line in inp:
	print line.strip().split('\t')[5]
	if int(line.strip().split('\t')[5])==0:
		out.write(line)
inp.close()
out.close()
