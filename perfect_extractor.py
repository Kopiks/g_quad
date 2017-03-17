#extract "perfect" Gqs -> score == 0 in gff file
import sys

inp = open(sys.argv[1],"r")
out = open(sys.argv[2],"w")
for line in inp:
	print line.strip().split('\t')[5]
	if int(line.strip().split('\t')[5])==0:
		out.write(line)
inp.close()
out.close()
