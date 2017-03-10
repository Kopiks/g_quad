

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
						"java -jar $picard "
						"MarkDuplicates "
						"INPUT=%s "
						"OUTPUT=%s "
						"METRICS_FILE=%s "
						"OPTICAL_DUPLICATE_PIXEL_DISTANCE=2500 "
						"CREATE_INDEX=true "
						#"QUIET=true"
						%(output+"_pre.bam", output+".bam", output+"_metrics.txt")
					)

			groups =(	
						"samtools sort "
						"%s |"
						"java -jar $picard "
						"AddOrReplaceReadGroups "
						"I=/dev/stdin "
						"O=%s "
						"RGID=UNKNOWN "
						"RGLB=UNKNOWN "
						"RGPL=UNKNOWN "
						"RGPU=UNKNOWN "
						"RGSM=%s "
						#"QUIET=true "
						"COMPRESSION_LEVEL=0 "
						"TMP_DIR=/tmp"
						%(file, output+"_pre.bam", filename)
					)


			subprocess.call(groups, shell=True) #os.system(groups)

			
			subprocess.call(dupli, shell=True) #os.system(dupli)
			try:
				os.remove(output+"_pre.bam")
			except OSError:
				pass
			
def main():
	pf = getFiles()
	addGroups(pf['path'], pf['files'])
	return 0
main();
