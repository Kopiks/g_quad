

import os
import subprocess

def getFiles():
	path = os.getcwd()				#get current working directory
	pre_files = os.listdir(path)		#list all files in a directory
	files = [x for x in pre_files if x.endswith(".bam")] #leave bams only
	return {'files':files, 'path':path}



def addGroups(path,files):
	"""
	Adds read groups and mark duplicates using picard
	"""
	if not os.path.exists("ReadGroups"):
		os.makedirs("ReadGroups")
	for file in files:
			filename = file.split(".")[0] #SRR number
			print filename
			output = "%s/ReadGroups/%s"%(path,filename)

			dupli = (
						"java -Xmx4G -jar $picard "
						"MarkDuplicates "
						"INPUT=%s "
						"OUTPUT=%s "
						"METRICS_FILE=%s "
						"OPTICAL_DUPLICATE_PIXEL_DISTANCE=2500 "
						"CREATE_INDEX=true "
						"REMOVE_DUPLICATES=true"
						#"QUIET=true"
						%(output+"_pre.bam", output+".bam", output+"_metrics.txt")
					)
			sort = (

						"samtools sort %s "
						"-@ 1 -m 4G -o %s &&"
						"samtools index %s"
						%(file, "pre_"+file, "pre_"+file)

					)
			groups =(	
						"samtools view "
						"-b -u %s "
						"Chr1 Chr2 Chr3 Chr4 Chr5 | "
						"java -Xmx4G -jar $picard "
						"AddOrReplaceReadGroups "
						"I=/dev/stdin "
						"O=%s "
						"RGID=UNKNOWN "
						"RGLB=UNKNOWN "
						"RGPL=ILLUMINA "
						"RGPU=UNKNOWN "
						"RGSM=%s "
						#"QUIET=true "
						"COMPRESSION_LEVEL=0 "
						"TMP_DIR=/tmp"
						%("pre_"+file, output+"_pre.bam", filename)
					)

			subprocess.call(sort, shell=True)

			subprocess.call(groups, shell=True) #os.system(groups)

			
			subprocess.call(dupli, shell=True) #os.system(dupli)
			try:
				os.remove(output+"_pre.bam")
				os.remove("pre_"+file)
				os.remove("pre_"+file+".bai")
			except OSError:
				pass
			
def mainBams():
	pf = getFiles()
	addGroups(pf['path'], pf['files'])
	return 0

if __name__ == '__main__':

	mainBams()
