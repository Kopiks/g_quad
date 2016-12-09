var_in=open("filtered_prom_s_var_raw.vcf", "r")
for line in var_in:
	if not line.startswith("#"):
		line=line.split("\t")[7]
		info=line.split(";")
		if info[0]=="INDEL": info[0]="INDEL=1"
		print info
		dic=dict(item.split("=") for item in info)
		print dic["AC"]
		if dic["AC"]==2:
			
			
