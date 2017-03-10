import sys

file_ = open(sys.argv[1],"r")
for line in file_:
	split_=line.replace(":","-")
	split_=split_.replace("\n","")
	split_=split_.split("-")
	if len(split_)<3:
		split_.append(split_[1])
	print('\t'.join(map(str,split_)))

