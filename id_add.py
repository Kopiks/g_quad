"""
Adds ID of the corresponding gene to the GFF output.
input:
bedtools intersect -a -b -wb |
"""

import sys
import re

for line in sys.stdin:					#from standard input
	read = line.split("\t")				#split tab delimited double-gff3 and assign it to "read" variable
	ann = re.split("[;:\-]+",read[17])	#split annotation field of 2nd gff3 record in a "read", ;:- 
	for n in ann:						
		if n.startswith("ID"):			#if item from previous split starts with ID
			temp = n					#append it to n variable
	read = read[:9]						#slice the read, leaving only first gff3
	read[8] = read[8]+";"+temp			#append ID information to the last field

	print("\t".join(map(str,read)))		#print out tab delimited read




