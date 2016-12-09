var_in=open("filtered_prom_s_var_raw.vcf", "r");
	for line in var_in:
		if line.startswith("#"):
			line=line.split("\t")
			info=line[7].split(";")
			