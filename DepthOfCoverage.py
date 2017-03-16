import os 
import subprocess
import sys

def getFiles():
	path = os.getcwd()				#get current working directory
	pre_files = os.listdir(path)		#list all files in a directory
	files = [x for x in pre_files if x.endswith(".bam")] #leave bams only
	return {'files':files, 'path':path}

def getDepth():

	filpa = getFiles()
	files = ["-I "+x for x in filpa['files']]
	refseq = sys.argv[1]						#path to reference fasta


	dt 	= 	(
			 	"java -jar $GATK "
              	"-T DiagnoseTargets "
            	"-R %s "
              	"-L /home/piotr/Desktop/g_quad-master/g_quad/araport/inters.bed "
              	"-o diag.vcf "
              	%refseq
              	+(" ".join(files))
		)
	cmd = 	(	
				"java -jar $GATK " 
				"-T DepthOfCoverage "
				"-ct 10 "
				"-omitBaseOutput "
				"-L /home/piotr/Desktop/g_quad-master/g_quad/araport/inters.bed "
				"-o output "
				"-R %s "%refseq
				+(" ".join(files))
			)	 

	awk = 	(
				'''awk -F"\t" -v OFS="\t"'''
				''' '{printf("%s%s",$1,OFS); for(i=5; i<= NF;i+=6) printf("%s%s",$i,(i+6>NF?"\\n":OFS))}' '''   # \\n not to newline
				''' output.sample_interval_summary > interval_summary ''' 
			) 
	
	subprocess.call(dt, shell=True)
	#subprocess.call(cmd, shell=True)
	#subprocess.call(awk, shell=True)

def mainDepth():
	getFiles()
	getDepth()
	return 0


if __name__ == '__main__':
	mainDepth()
