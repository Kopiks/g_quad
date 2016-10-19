import pysam
import pybedtools

f_merge = open("merge.bed","r")
bam_i = pysam.AlignmentFile("outs.bam", "rb")

for line in f_merge:
	for i in bam_i.pileup(int(line.split("\t")[1]),int(line.split("\t")[2])):
		print line.split("\t")[1]
		for read in i.pileups:
			if not read.is_Del and not pileup.is_refskip:
				print read.alignment.query_sequence[pileupread.query_position]
		
f_merge.close()
bam_i.close()		
