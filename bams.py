import os
import subprocess

def getFiles():
	path = os.getcwd()				#get current working directory
	pre_files = os.listdir(path)		#list all files in a directory
	files = [x for x in pre_files if x.endswith(".bam")] #leave bams only
	return {'files':files, 'path':path}



def addGroups():
	"""
	Adds read groups using picard
	"""
	os.makedirs("ReadGroups")
	for file in files:
			filename = ".".join(file.split(".")[:-2]) #SRR number
			output = "%s/ReadGroups/%s"%(path,filename[0]+".bam")
			subprocess.call("java -jar $picard AddOrReplaceReadGroups I=%s O=%s RGID=- RGLB=- RGPL=- RGPU=- RGSM=%s" %(file, output, filename), shell=True)
"""
def markDuplicates():
	for file in files:

"""
print getFiles()